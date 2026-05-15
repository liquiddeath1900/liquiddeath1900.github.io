# SeamlessFlow Dashboard — Auth Setup

The code changes are done. Three things still need to happen in admin UIs you control:

1. Supabase URL allowlist (Auth → URL Configuration)
2. Google Cloud OAuth client (authorized origins + redirect URIs)
3. RLS policies on every table the dashboard reads (CRITICAL — without this, the login is decorative)

Do them in order. Total time: ~10 minutes.

---

## 1. Supabase — Add seamlessflow.ai to redirect URLs

Open the project: <https://supabase.com/dashboard/project/lpzijtmbdowcshomyenk/auth/url-configuration>

**Site URL:** leave whatever's there for yerramazing (`https://yerramazing.com`) — Site URL is only used as the fallback redirect; per-page `emailRedirectTo` overrides it.

**Redirect URLs — Add these:**

```
https://seamlessflow.ai/**
https://www.seamlessflow.ai/**
http://localhost:8000/**
```

Save.

---

## 2. Google Cloud — Add seamlessflow.ai to OAuth client

The OAuth client is the existing yerramazing one (client ID `739242878281-j4738945olk0o5d6m5p92h2810t48nkg.apps.googleusercontent.com`).

Open: <https://console.cloud.google.com/apis/credentials> → project **yerramazing** → click that client.

**Authorized JavaScript origins — Add:**

```
https://seamlessflow.ai
https://www.seamlessflow.ai
http://localhost:8000
```

**Authorized redirect URIs — Add:**

```
https://seamlessflow.ai/login.html
https://www.seamlessflow.ai/login.html
https://lpzijtmbdowcshomyenk.supabase.co/auth/v1/callback
http://localhost:8000/login.html
```

The `supabase.co/auth/v1/callback` one is probably already there (yerramazing uses it).

**Test users (if app is still in Testing mode):**
APIs & Services → OAuth consent screen → Test users → Add `seamlessflow.ai@gmail.com`.

Save.

---

## 3. Supabase — RLS policies (THE IMPORTANT ONE)

**Why this matters:** the Supabase anon key is in the HTML source on dashboard.html (anyone can view-source and grab it). Without RLS, that anon key gives anyone full read access to your tables — login or no login. RLS is what makes "they need to sign in" actually true.

Open SQL editor: <https://supabase.com/dashboard/project/lpzijtmbdowcshomyenk/sql/new>

Paste this and run it. Adjust the table names if any of them don't exist yet — the `sf_dashboard_*` family won't exist until LM ships Task 5.

```sql
-- ====================================================================
-- Enable RLS on every table the dashboard reads.
-- Policy: only the allowlisted email (seamlessflow.ai@gmail.com) can read.
-- Service role bypasses RLS entirely (so LM's nightly sync still writes).
-- ====================================================================

-- Helper: function returns true if the caller's JWT belongs to an allowed email.
CREATE OR REPLACE FUNCTION public.is_sf_owner()
RETURNS boolean
LANGUAGE sql STABLE
AS $$
  SELECT lower(coalesce(auth.jwt() ->> 'email', '')) IN (
    'seamlessflow.ai@gmail.com'
  );
$$;

-- Apply to existing SF dashboard tables (the ones the page already queries).
-- If a table doesn't exist yet, skip its block — re-run after LM creates it.

DO $$
DECLARE
  t text;
  tables text[] := ARRAY[
    -- Existing SF audit/site tables (rename to match your real table names)
    'seo_audits',
    'sf_scan_history',
    -- Future sf_dashboard_* tables (LM creates these in Task 5)
    'sf_dashboard_keywords',
    'sf_dashboard_prospects',
    'sf_dashboard_competitors',
    'sf_dashboard_action_items',
    'sf_dashboard_content_ideas',
    'sf_dashboard_cntemup_leads',
    'sf_dashboard_audit_patterns',
    'sf_dashboard_outreach_log',
    'sf_dashboard_pipeline_health',
    'sf_dashboard_sync_log'
  ];
BEGIN
  FOREACH t IN ARRAY tables LOOP
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema='public' AND table_name=t) THEN
      EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY', t);
      EXECUTE format('DROP POLICY IF EXISTS sf_owner_read ON public.%I', t);
      EXECUTE format(
        'CREATE POLICY sf_owner_read ON public.%I FOR SELECT TO authenticated USING (public.is_sf_owner())',
        t
      );
      -- No INSERT/UPDATE/DELETE policy for authenticated → all writes must use service_role.
    END IF;
  END LOOP;
END $$;
```

**To verify:** after running, open dashboard.html in a private window. Without logging in, Network tab should show 200 responses but empty arrays (`[]`). After logging in as the allowlisted email, you should see real rows.

---

## 4. (Optional) Disable email signups for everyone but you

If the form somehow gets abused (bots filling in random emails to trigger magic links), you can lock it down further:

Auth → Providers → Email → **Disable "Allow new users to sign up"**.

You'll need to sign in once first to create your user record; after that, flip this off.

---

## Quick test plan

1. Open `https://seamlessflow.ai/dashboard.html` in a fresh browser. Should redirect to `/login.html?redirect=dashboard.html`.
2. Click "Continue with Google" → pick `seamlessflow.ai@gmail.com` → should land back on dashboard.html with data visible and a "Sign out" button top-right.
3. Try with a different Google account → should get bounced to `/login.html?error=denied` with the "not authorized" message.
4. Open Network tab while logged in → confirm Supabase requests include an `Authorization: Bearer eyJ...` header that's NOT just the anon key (it should be the user's session JWT).

---

## When LM finally ships Task 5

LM creates the `sf_dashboard_*` tables. Re-run the SQL block in section 3 (it's idempotent — `DROP POLICY IF EXISTS` makes it safe). The DO block automatically skips tables that don't exist yet.
