// seamlessflow.ai — Supabase Config
//
// IMPORTANT — this anon key is intentionally public-readable:
//
// The Supabase anon key is *designed* to ship in browser code. It only confers
// the permissions of the unauthenticated `anon` role. Real protection comes
// from Row Level Security:
//
//   1. All sf_dashboard_* tables have RLS enabled
//   2. Policy `sf_owner_read` only returns rows when auth.jwt() email matches
//      seamlessflow.ai@gmail.com (see is_sf_owner() function)
//   3. With no session, queries return [] — anon key alone is useless
//
// If you ever rotate this key, also rotate the publishable key in
// Supabase dashboard → Settings → API. The RLS policies travel with the DB.
//
// Semgrep flags this as "JWT detected (ERROR)" — that rule does not understand
// Supabase's split-key model and is a known false positive here.
const SUPABASE_URL = 'https://lpzijtmbdowcshomyenk.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxwemlqdG1iZG93Y3Nob215ZW5rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQwNTM4MDgsImV4cCI6MjA4OTYyOTgwOH0.2GN7eyC8rutMuHrVOc_2e2meMLu1S5YoNViV1zFgzX4';
