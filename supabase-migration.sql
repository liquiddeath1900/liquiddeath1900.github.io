-- ============================================
-- SEAMLESSFLOW TABLES → YERRAMAZING SUPABASE
-- ============================================
-- Run this in yerramazing Supabase SQL Editor
-- All tables prefixed with sf_ to avoid conflicts
-- ============================================

-- 1. SEO Audit History (weekly audit scores)
CREATE TABLE sf_audit_history (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    domain TEXT NOT NULL,
    audit_date DATE NOT NULL,
    overall_score INTEGER,
    technical_score INTEGER,
    speed_score INTEGER,
    mobile_score INTEGER,
    onpage_score INTEGER,
    security_score INTEGER,
    lcp_ms NUMERIC,
    fcp_ms NUMERIC,
    ttfb_ms NUMERIC,
    cls NUMERIC
);
CREATE INDEX idx_sf_audit_domain_date ON sf_audit_history(domain, audit_date DESC);

-- 2. Weekly AI Insights
CREATE TABLE sf_weekly_insights (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    domain TEXT NOT NULL,
    week_start DATE NOT NULL,
    top_wins JSONB DEFAULT '[]',
    critical_issues JSONB DEFAULT '[]',
    recommended_tactics JSONB DEFAULT '[]'
);
CREATE INDEX idx_sf_insights_domain ON sf_weekly_insights(domain, week_start DESC);

-- 3. Google Algorithm Updates
CREATE TABLE sf_google_updates (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    detected_date DATE NOT NULL,
    update_name TEXT,
    description TEXT,
    impact_level TEXT,
    source_url TEXT
);
CREATE INDEX idx_sf_updates_date ON sf_google_updates(detected_date DESC);

-- 4. Local Rankings (Local Falcon geo-grid data)
CREATE TABLE sf_local_rankings (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    domain TEXT NOT NULL,
    keyword TEXT NOT NULL,
    location TEXT,
    grid_size TEXT,
    avg_rank NUMERIC,
    top_3_pct NUMERIC,
    top_10_pct NUMERIC,
    not_ranking_pct NUMERIC,
    scan_date TIMESTAMPTZ,
    raw_data JSONB
);
CREATE INDEX idx_sf_rankings_domain ON sf_local_rankings(domain, scan_date DESC);

-- 5. Site Changes Log
CREATE TABLE sf_changes_log (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    domain TEXT NOT NULL,
    change_date DATE NOT NULL,
    change_type TEXT,
    description TEXT,
    details JSONB
);
CREATE INDEX idx_sf_changes_domain ON sf_changes_log(domain, change_date DESC);

-- 6. Chatbot Leads
CREATE TABLE sf_chatbot_leads (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    email TEXT NOT NULL,
    goal TEXT,
    business_type TEXT,
    challenge TEXT,
    timeline TEXT,
    team_size TEXT,
    wants_call BOOLEAN DEFAULT FALSE,
    transcript TEXT,
    source TEXT,
    funnel_type TEXT,
    is_mobile BOOLEAN,
    bypass_attempts INTEGER DEFAULT 0,
    page_url TEXT,
    qualified BOOLEAN DEFAULT FALSE
);
CREATE INDEX idx_sf_leads_email ON sf_chatbot_leads(email);
CREATE INDEX idx_sf_leads_created ON sf_chatbot_leads(created_at DESC);
CREATE INDEX idx_sf_leads_qualified ON sf_chatbot_leads(qualified) WHERE qualified = TRUE;

-- 7. Leads (from lead intake form / n8n)
CREATE TABLE sf_leads (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    email TEXT,
    business_name TEXT,
    website_url TEXT,
    phone TEXT,
    service_area TEXT,
    business_type TEXT,
    source TEXT,
    status TEXT DEFAULT 'new'
);
CREATE INDEX idx_sf_leads_status ON sf_leads(status);

-- ============================================
-- ENABLE ROW LEVEL SECURITY (allow anon reads)
-- ============================================
ALTER TABLE sf_audit_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE sf_weekly_insights ENABLE ROW LEVEL SECURITY;
ALTER TABLE sf_google_updates ENABLE ROW LEVEL SECURITY;
ALTER TABLE sf_local_rankings ENABLE ROW LEVEL SECURITY;
ALTER TABLE sf_changes_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE sf_chatbot_leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE sf_leads ENABLE ROW LEVEL SECURITY;

-- Allow anon key to read all tables (dashboard needs this)
CREATE POLICY "Allow anon read" ON sf_audit_history FOR SELECT USING (true);
CREATE POLICY "Allow anon read" ON sf_weekly_insights FOR SELECT USING (true);
CREATE POLICY "Allow anon read" ON sf_google_updates FOR SELECT USING (true);
CREATE POLICY "Allow anon read" ON sf_local_rankings FOR SELECT USING (true);
CREATE POLICY "Allow anon read" ON sf_changes_log FOR SELECT USING (true);
CREATE POLICY "Allow anon read" ON sf_chatbot_leads FOR SELECT USING (true);
CREATE POLICY "Allow anon read" ON sf_leads FOR SELECT USING (true);

-- Allow anon key to insert (n8n workflows write via anon key)
CREATE POLICY "Allow anon insert" ON sf_audit_history FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow anon insert" ON sf_weekly_insights FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow anon insert" ON sf_google_updates FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow anon insert" ON sf_local_rankings FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow anon insert" ON sf_changes_log FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow anon insert" ON sf_chatbot_leads FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow anon insert" ON sf_leads FOR INSERT WITH CHECK (true);

-- ============================================
-- DONE! Tables are ready for SeamlessFlow data.
-- Next: update dashboard.html + n8n workflows
-- to use yerramazing's Supabase URL + key
-- ============================================
