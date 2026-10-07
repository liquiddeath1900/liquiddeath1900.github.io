-- Discovery call funnel leads (book-call.html).
-- Run once in Supabase SQL editor (project lpzijtmbdowcshomyenk).
-- anon can INSERT only. No SELECT/UPDATE/DELETE policy for anon = leads are not readable with the public key.
create table if not exists public.sf_discovery_requests (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  name text not null check (char_length(name) between 1 and 120),
  business_name text not null check (char_length(business_name) between 1 and 160),
  email text not null check (char_length(email) between 3 and 200),
  phone text not null check (char_length(phone) between 1 and 40),
  social_url text check (char_length(social_url) <= 300),
  goal text not null check (char_length(goal) <= 100),
  timeline text not null check (char_length(timeline) <= 100),
  package_interest text check (char_length(package_interest) <= 100),
  accounts text check (char_length(accounts) <= 200),
  source text check (char_length(source) <= 50),
  status text not null default 'new'
);
alter table public.sf_discovery_requests enable row level security;
revoke all on public.sf_discovery_requests from anon, authenticated;
grant insert (name, business_name, email, phone, social_url, goal, timeline, package_interest, accounts, source)
  on public.sf_discovery_requests to anon;
create policy "anon can submit discovery request"
  on public.sf_discovery_requests for insert to anon with check (status = 'new');
-- Owner reads via dashboard (is_sf_owner() already exists for sf_dashboard_* tables)
grant select, update on public.sf_discovery_requests to authenticated;
create policy "owner reads discovery requests"
  on public.sf_discovery_requests for select to authenticated using (public.is_sf_owner());
create policy "owner updates discovery requests"
  on public.sf_discovery_requests for update to authenticated using (public.is_sf_owner()) with check (public.is_sf_owner());
