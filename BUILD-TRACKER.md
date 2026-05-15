# SeamlessFlow Proprietary Software Build

**Why this exists:** Replace paid tools (Local Falcon, BrightLocal, Loom) with owned software. Lower costs, custom branding, IP moat, no subscription churn.

**Goal:** Match LF/BL feature parity for client deliverables. Variable cost (per API call) instead of fixed monthly subscription.

**Started:** 2026-05-09
**Status:** Planning → Build phase 1

---

## Cost Math (the why)
- **Before:** LF (~$129-249/mo) + BL (~$39-79/mo) + Loom ($12.50/mo) = **~$200-340/mo fixed**
- **After:** Google Places API ($1.30/scan) + scraping (free) + own infra = **~$50-100/mo variable**
- **Break-even:** Pays for itself in 1 month if we use it on 5+ client sites

---

## Build Components

### 1. Geo-grid Scanner (replaces Local Falcon) — HIGHEST PRIORITY
**Status:** Not started
**Owner:** TBD (probably main, can hand pieces to LM)
**Estimate:** 3-5 days

**What it does:**
- Input: business name, primary location (lat/lng), keyword list, grid size (5x5/7x7/9x9/13x13)
- For each grid coordinate, query Google Places API "nearby search" with the keyword
- Record where the target business ranks in local pack at that coordinate
- Output: heatmap PNG + raw JSON data

**Tech stack:**
- Python (asyncio for parallel grid queries)
- Google Places API (Place Details + Nearby Search) — pay per call
- Pillow or matplotlib for heatmap rendering
- SQLite for scan history

**API options to evaluate:**
- [ ] Google Places API — official, $17/1000 calls, most reliable
- [ ] SerpAPI — $50/mo for 5000 searches, includes local pack
- [ ] DataForSEO — pay-as-you-go, cheaper for high volume
- [ ] Direct scraping — free but breaks every Google update

**Steps:**
- [ ] Pick API (recommend: SerpAPI for MVP, switch to Places API if scaling)
- [ ] Build coordinate generator (lat/lng grid around center point)
- [ ] Build scan runner (async, rate-limited)
- [ ] Build rank parser (find target in local pack results)
- [ ] Build heatmap renderer
- [ ] CLI wrapper: `geo-grid scan --site=X --keyword=Y --grid=7x7`
- [ ] Save to Supabase `sf_scan_history` (schema exists from earlier work)

---

### 2. Citation Checker (replaces BrightLocal) — MEDIUM PRIORITY
**Status:** Not started
**Owner:** TBD
**Estimate:** 2-3 days

**What it does:**
- Input: business NAP (name, address, phone)
- Check 50 common directories for: presence + NAP consistency + listing URL
- Output: report — found/missing/inconsistent for each directory

**Directory targets (start with top 20):**
- Yelp, BBB, Foursquare, Apple Maps, Yellow Pages, MapQuest, Citysearch, Bing Places, Facebook, Manta, Whitepages, Hotfrog, Brownbook, Cybo, Cylex, EZlocal, Bizapedia, Showmelocal, AmericanTowns, Local.com
- Cannabis-specific: Weedmaps, Leafly, Dutchie, AllBud, Pot Guide

**Tech stack:**
- Python + httpx + BeautifulSoup
- Per-directory adapters (each scrapes/queries differently)
- Fuzzy matching (rapidfuzz) for NAP consistency

**Steps:**
- [ ] Build directory adapter base class
- [ ] Implement top 10 directory adapters
- [ ] Build NAP fuzzy matcher (catches "St." vs "Street" etc.)
- [ ] Build report aggregator
- [ ] CLI: `citation check --name=X --address=Y --phone=Z`

---

### 3. PDF Report Builder — LOW PRIORITY (build after scanner works)
**Status:** Not started
**Estimate:** 1-2 days

**What it does:**
- Take outputs from #1 and #2, generate branded SeamlessFlow PDF
- Cover page, geo-grid heatmap, citation table, recommendations

**Tech stack:**
- Python + WeasyPrint or ReportLab
- HTML/CSS templates (so it matches site branding)

---

### 4. Audit Pattern Miner — QUICK WIN
**Status:** Bridged to LM 2026-05-09
**Owner:** LM (server instance)
**Estimate:** 1 day for LM

**What it does:**
- Pull all audit data from LM Mac (MD/JSON files)
- Find cross-audit patterns: "X% of audits had issue Y"
- Output: JSON + summary MD → fuels content/filming scripts

**Why LM:** It has the audit data locally; no need to copy files around.

---

## Cadence
- Update this file every time a component status changes
- Update `~/TODO.md` when blockers surface
- Bridge handoffs to LM via `claude-bridge/handoff/`

## Decisions Log
- **2026-05-09:** Drop LF/BL/Loom subscriptions. Build proprietary. (Cost not justified by results — 1 click in 28 days from SEO indicated outreach is the path, not better tools.)
- **2026-05-09:** Use SerpAPI for geo-grid MVP (cheapest entry, predictable pricing).

## Blockers
- (none yet)
