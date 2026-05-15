#!/usr/bin/env python3
"""
Push local JSON exports → Supabase sf_dashboard_* tables.

Uses the Supabase Personal Access Token from macOS keychain to fetch the project's
service_role key, then writes via PostgREST. service_role bypasses RLS.

Idempotent — runs UPSERT/REPLACE so you can run this every time the data changes.

Reads:  seamlessflow-site/data/*.json (must exist — run export-bridge-data.py + generate-content-briefs.py first)
Writes: Supabase project lpzijtmbdowcshomyenk, tables sf_dashboard_*
"""

import json
import subprocess
import sys
import urllib.error
import urllib.request
from base64 import b64decode
from pathlib import Path

PROJECT_REF = "lpzijtmbdowcshomyenk"
SUPABASE_URL = f"https://{PROJECT_REF}.supabase.co"
MGMT_API = "https://api.supabase.com"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def get_supabase_pat():
    """Pull the Supabase Personal Access Token from macOS keychain."""
    result = subprocess.run(
        ["security", "find-generic-password", "-s", "Supabase CLI", "-a", "supabase", "-w"],
        capture_output=True, text=True, check=True,
    )
    raw = result.stdout.strip()
    if raw.startswith("go-keyring-base64:"):
        return b64decode(raw[len("go-keyring-base64:"):]).decode().strip()
    return raw


def get_service_role_key(pat):
    """Fetch the service_role API key via Management API. Uses curl — urllib gets 403."""
    result = subprocess.run(
        [
            "curl", "-sS", "-H", f"Authorization: Bearer {pat}",
            f"{MGMT_API}/v1/projects/{PROJECT_REF}/api-keys?reveal=true",
        ],
        capture_output=True, text=True, check=True,
    )
    keys = json.loads(result.stdout)
    for k in keys:
        if k.get("name") == "service_role":
            return k["api_key"]
    raise SystemExit(f"Could not find service_role key in response: {result.stdout[:200]}")


def load_json(name):
    path = DATA_DIR / name
    if not path.exists():
        print(f"  ⚠️  {name} not found at {path} — skipping")
        return None
    return json.loads(path.read_text())


def post_to_supabase(table, rows, key, conflict=None):
    """UPSERT rows via PostgREST. Returns (count, error)."""
    if not rows:
        return 0, None

    url = f"{SUPABASE_URL}/rest/v1/{table}"
    if conflict:
        url += f"?on_conflict={conflict}"

    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates,return=minimal",
    }
    body = json.dumps(rows, default=str).encode()
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return len(rows), None
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        return 0, f"HTTP {e.code}: {err[:300]}"
    except Exception as e:
        return 0, str(e)


def truncate(table, key):
    """Wipe a table before re-loading (when no natural PK or to ensure clean state)."""
    url = f"{SUPABASE_URL}/rest/v1/{table}?id=gte.0"
    headers = {"apikey": key, "Authorization": f"Bearer {key}", "Prefer": "return=minimal"}
    req = urllib.request.Request(url, headers=headers, method="DELETE")
    try:
        urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        pass  # likely empty already


def main():
    pat = get_supabase_pat()
    print(f"PAT loaded: sbp_{'*' * 8} (length {len(pat)})")
    service_key = get_service_role_key(pat)
    print(f"service_role key loaded (length {len(service_key)})")
    print(f"Data dir: {DATA_DIR}")
    print("")

    # ── Tables with natural PK (id column) → simple upsert by id ──
    simple_tables = [
        ("sf_dashboard_prospects",      "prospects.json",      "id"),
        ("sf_dashboard_action_items",   "action_items.json",   "id"),
        ("sf_dashboard_cntemup_leads",  "cntemup_leads.json",  "id"),
        ("sf_dashboard_outreach",       "outreach.json",       "id"),
    ]
    for table, fname, conflict in simple_tables:
        rows = load_json(fname)
        if rows is None:
            continue
        # Strip computed/extra fields not in the schema for outreach
        if table == "sf_dashboard_outreach":
            for r in rows:
                r.pop("qualification_score", None) if False else None  # keep — column exists
        count, err = post_to_supabase(table, rows, service_key, conflict=conflict)
        print(f"  {table}: {'OK' if not err else 'ERR'} ({count} rows) {err or ''}")

    # ── Competitors (rolled up): UPSERT by agency_name ──
    rows = load_json("competitors.json") or []
    count, err = post_to_supabase("sf_dashboard_competitors", rows, service_key, conflict="agency_name")
    print(f"  sf_dashboard_competitors: {'OK' if not err else 'ERR'} ({count} rows) {err or ''}")

    # ── Competitor activity feed: dedup-by-(date,agency,activity_type) ──
    rows = load_json("competitor_activity.json") or []
    # Clean missing source_file column if present
    for r in rows:
        r.pop("source_file", None)
    count, err = post_to_supabase("sf_dashboard_competitor_activity", rows, service_key, conflict="date,agency_name,activity_type")
    print(f"  sf_dashboard_competitor_activity: {'OK' if not err else 'ERR'} ({count} rows) {err or ''}")

    # ── Keywords: composite PK (site, keyword) ──
    rows = load_json("keywords.json") or []
    count, err = post_to_supabase("sf_dashboard_keywords", rows, service_key, conflict="site,keyword")
    print(f"  sf_dashboard_keywords: {'OK' if not err else 'ERR'} ({count} rows) {err or ''}")

    # ── Content ideas: UPSERT by (site, title) ──
    rows = load_json("content_ideas.json") or []
    count, err = post_to_supabase("sf_dashboard_content_ideas", rows, service_key, conflict="site,title")
    print(f"  sf_dashboard_content_ideas: {'OK' if not err else 'ERR'} ({count} rows) {err or ''}")

    # ── Content briefs: PK is text id ──
    briefs_doc = load_json("content_briefs.json")
    if briefs_doc:
        rows = briefs_doc.get("briefs", [])
        count, err = post_to_supabase("sf_dashboard_content_briefs", rows, service_key, conflict="id")
        print(f"  sf_dashboard_content_briefs: {'OK' if not err else 'ERR'} ({count} rows) {err or ''}")

    # ── Summary: store as a single key ──
    summary = load_json("summary.json")
    if summary:
        summary_row = {"key": "main", "value": summary}
        count, err = post_to_supabase("sf_dashboard_summary", [summary_row], service_key, conflict="key")
        print(f"  sf_dashboard_summary: {'OK' if not err else 'ERR'} ({count} rows) {err or ''}")

    # ── Log this sync ──
    from datetime import datetime
    log_row = {
        "sync_ended": datetime.now().isoformat(),
        "status": "success",
        "rows_synced": 0,  # could total above
    }
    post_to_supabase("sf_dashboard_sync_log", [log_row], service_key)

    print("")
    print("Done. Verify in Supabase dashboard or run a SELECT.")


if __name__ == "__main__":
    main()
