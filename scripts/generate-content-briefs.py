#!/usr/bin/env python3
"""
Turn raw pipeline data into structured content briefs (hook + reel outline + YouTube angle + sources).

NOT full scripts — just enough scaffolding to walk into a /content-shoot session with the data already in place.

Voice rules (locked, see project_content_voice_hybrid.md):
- Hooks: 1–2 sentences max
- Reel body: short-phrase bullets with > o * markers (> mandatory, o optional, * land/close)
- YouTube angle: expand, never repeat the reel
- No symbols in YouTube blocks (=, →, ~, %, M, B, w/) — spell out
- One NYC analogy per segment max
- No "deliver with intensity" / "let it land" — concrete delivery cues only

Reads:
  ~/Documents/CNTEMUP/claude-bridge/data/bridge.db

Writes:
  seamlessflow-site/data/content_briefs.json
"""

import json
import re
import sqlite3
from collections import Counter
from datetime import datetime
from pathlib import Path

HOME = Path.home()
BRIDGE_DB = HOME / "Documents/CNTEMUP/claude-bridge/data/bridge.db"
OUT_FILE = HOME / "Documents/SeamLessFlow/seamlessflow-site/data/content_briefs.json"


# ── Audit-pattern mining ─────────────────────────────────────────────

# Phrase buckets we look for in prospect outreach_angles.
# Each = (label, keywords-or-phrases that trigger it).
GAP_BUCKETS = [
    ("Google Business Profile not optimized",   ["gbp", "google business profile", "google business", "map pack"]),
    ("No schema markup",                         ["schema", "structured data", "json-ld"]),
    ("No local/neighborhood content",            ["local content", "neighborhood", "borough", "no local"]),
    ("Thin or missing blog content",             ["no blog", "blog", "thin content", "content foundation"]),
    ("Indexing or crawlability problem",         ["indexed", "page indexed", "one page", "not indexed", "robots", "noindex"]),
    ("Leafly / Weedmaps eating their traffic",   ["leafly", "weedmaps", "directory", "directories"]),
    ("Review velocity / Leafly reviews missing", ["0 leafly", "no reviews", "zero reviews", "review velocity"]),
    ("First-mover window closing",               ["first-mover", "first mover", "wide open", "unclaimed", "window"]),
    ("Age-gate blocking Googlebot",              ["age gate", "age-gate", "blocking googlebot"]),
    ("NAP inconsistency",                        ["nap", "name address phone", "inconsistent"]),
]


def mine_gaps(prospects):
    """Count prospects whose outreach_angle matches each gap bucket."""
    counts = Counter()
    samples = {label: [] for label, _ in GAP_BUCKETS}
    total_with_angle = 0
    for p in prospects:
        angle = (p.get("outreach_angle") or "").lower()
        if not angle:
            continue
        total_with_angle += 1
        matched_here = set()
        for label, kws in GAP_BUCKETS:
            for kw in kws:
                if kw in angle and label not in matched_here:
                    counts[label] += 1
                    if len(samples[label]) < 3:
                        samples[label].append({
                            "business": p.get("business_name"),
                            "location": p.get("location"),
                        })
                    matched_here.add(label)
                    break
    return {"counts": counts, "samples": samples, "total": total_with_angle}


# ── Brief builders ───────────────────────────────────────────────────


def brief_audit_pattern(gap_label, count, total, samples):
    pct = round(count / total * 100) if total else 0
    title = f"{count} of {total} NYC dispensaries we audited: {gap_label.lower()}"
    hook = (
        f"We pulled up {total} licensed New York dispensaries and checked their websites. "
        f"{count} of them — that's {pct} percent — had the same gap."
    )
    reel_outline = [
        f"> {total} NYC dispensaries audited",
        f"> {count} of them ({pct} percent) hit the same wall: {gap_label.lower()}",
        f"o not a guess — checked each one",
        f"o cheapest fix in cannabis SEO right now",
        f"* land: the percent that fix this first will own the borough",
    ]
    youtube_angle = (
        "Walk through three example dispensaries with this exact gap, screen-recorded. "
        "Explain why it kills map-pack visibility, then show the before-and-after of a 20-minute fix. "
        "End with what the audit actually looks for — invitation to send a site for free check."
    )
    sample_text = " · ".join([s["business"] for s in samples if s.get("business")][:3])
    return {
        "id": f"pattern-{re.sub(r'[^a-z0-9]+', '-', gap_label.lower()).strip('-')}",
        "type": "audit_pattern",
        "weight": count * 2,
        "title": title,
        "hook": hook,
        "reel_outline": reel_outline,
        "youtube_angle": youtube_angle,
        "why_now": f"Standing inventory of {total} prospects we've already audited. The stat is real, the angle is open.",
        "data_pull": f"Mined from prospects.outreach_angle ({count}/{total} matched)",
        "examples": sample_text or None,
        "sources": [],
        "delivery_cues": [
            f'// Slow on "{count} of {total}." Let the number land.',
            f'// Flat tone on the {pct} percent. Numbers don\'t need volume.',
        ],
    }


def brief_competitor_counter(activity_row):
    agency = activity_row["agency_name"]
    detail = (activity_row.get("detail") or "").strip()
    threat = (activity_row.get("threat_level") or "").upper()
    date = activity_row.get("date") or ""
    source_url = activity_row.get("source_url")

    short_detail = detail.split(".")[0][:160]

    title = f"{agency} just made a move. The part nobody's saying out loud."
    hook = (
        f"A {('competing' if threat == 'HIGH' else '')} marketing agency in the cannabis space "
        f"just published something. The numbers look good. The framing isn't."
    ).strip()

    reel_outline = [
        f"> {agency} published this {date}",
        f"> their claim: {short_detail.lower() if short_detail else 'see source'}",
        "o what they're not saying",
        "o the assumption underneath that doesn't hold up",
        "* land: the dispensary that hires on this framing pays for the agency's learning curve",
    ]

    youtube_angle = (
        f"Steel-man {agency}'s claim first — strongest possible version of their argument. "
        "Then walk through the counter-evidence from our own audit data. "
        "Close with what an owner-operator should actually look for in an agency this quarter."
    )

    sources = []
    if source_url:
        sources.append({"label": f"{agency} source", "url": source_url})

    return {
        "id": f"comp-{re.sub(r'[^a-z0-9]+', '-', agency.lower()).strip('-')}-{date}",
        "type": "competitor_counter",
        "weight": 100 if threat == "HIGH" else 50,
        "title": title,
        "hook": hook,
        "reel_outline": reel_outline,
        "youtube_angle": youtube_angle,
        "why_now": f"{agency} active as of {date}. Threat level: {threat or 'unspecified'}.",
        "data_pull": f"competitor_activity row dated {date}",
        "examples": None,
        "sources": sources,
        "delivery_cues": [
            f'// Pause on "{agency}." Let it sit a beat.',
            '// Flat on the steel-man. No sarcasm.',
        ],
    }


def brief_keyword_movement(kw):
    keyword = kw["keyword"]
    site = kw["site"]
    delta = kw.get("delta")
    first = kw.get("first_position")
    last = kw.get("latest_position")

    direction = "climbed" if delta and delta > 0 else "dropped" if delta and delta < 0 else "moved"
    abs_delta = abs(delta) if delta else 0

    title = f"\"{keyword}\" {direction} {abs_delta} spots — here's what changed"
    hook = (
        f"We've been tracking this keyword on our own site every day. "
        f"It {direction} from position {first} to {last}. Here's what we actually did."
    )

    reel_outline = [
        f"> tracking: {keyword}",
        f"> position {first} on day one. position {last} now.",
        f"o what moved it: page changes, links, indexing",
        f"o what didn't move it: most of what agencies sell",
        f"* land: rank tracking only matters if you know which change caused the move",
    ]

    youtube_angle = (
        "Pull up the actual Search Console data. Show the inflection point on the line. "
        "Walk through every change made in the two weeks before the move — schema, internal links, content, etc. "
        "Make the case for change-logged SEO: every action dated, every effect attributed."
    )

    return {
        "id": f"kw-{re.sub(r'[^a-z0-9]+', '-', keyword.lower()).strip('-')}",
        "type": "keyword_movement",
        "weight": 30 + abs_delta * 5,
        "title": title,
        "hook": hook,
        "reel_outline": reel_outline,
        "youtube_angle": youtube_angle,
        "why_now": f"Currently #{last} on {site}. Movement: {delta:+d}.",
        "data_pull": f"keyword_history series for '{keyword}' on {site}",
        "examples": None,
        "sources": [],
        "delivery_cues": [
            '// Slow on the two positions. Eye contact on the second one.',
            '// Drop volume on "most of what agencies sell."',
        ],
    }


def brief_reddit_response(lead):
    platform = (lead.get("platform") or "Reddit").strip()
    post_text = (lead.get("post_text") or "").strip()
    handle = lead.get("user_handle") or ""
    url = lead.get("post_url")
    suggested = (lead.get("suggested_response") or "").strip()
    region = lead.get("region")
    urgency = (lead.get("urgency") or "").lower()

    # Extract the first sentence as the question/topic
    topic = post_text.split("\n")[0][:140].strip().rstrip(":.")
    if not topic:
        return None

    title = f"{platform} thread: \"{topic[:80]}...\" — the answer nobody's giving"
    hook = (
        f"Someone on {platform} just asked a question. "
        "The top reply is wrong, and the second reply is incomplete. The real answer is short."
    )

    reel_outline = [
        f"> question: {topic[:100]}",
        f"o the popular answer",
        f"o why it's wrong",
        f"o what actually works",
        f"* land: drop the link, leave the door open",
    ]

    youtube_angle = (
        "Use the thread as a cold-open. Walk through three or four common bad answers people give in cannabis communities. "
        "Then the real one, with data. Close with how to find these threads — community marketing as discovery channel."
    )

    sources = []
    if url:
        sources.append({"label": f"{platform} thread", "url": url})

    return {
        "id": f"lead-{lead.get('id')}",
        "type": "reddit_response",
        "weight": 80 if urgency == "hot" else 40,
        "title": title,
        "hook": hook,
        "reel_outline": reel_outline,
        "youtube_angle": youtube_angle,
        "why_now": f"{platform} thread, {region or 'no region'}, urgency: {urgency or 'unspecified'}.",
        "data_pull": f"cntemup_leads row #{lead.get('id')}",
        "examples": (suggested[:300] + "…") if len(suggested) > 300 else suggested or None,
        "sources": sources,
        "delivery_cues": [
            '// Read the question deadpan.',
            '// Smile on "the real answer is short."',
        ],
    }


def brief_stale_opportunity(item):
    content = (item.get("content") or "").strip()
    days = item.get("carried_days") or 0
    if not content or days < 5:
        return None

    title = f"The 'we'll get to it' opportunity: {content[:80]}"
    hook = (
        f"This task has been sitting on our list for {days} days. "
        "Long enough that nobody's coming back to do it. Let's film about why instead."
    )

    reel_outline = [
        f"> task on the list {days} days: {content[:100]}",
        f"o agency lesson one: every list grows",
        f"o agency lesson two: rotting tasks become content",
        f"* land: the stuff you didn't ship is the story",
    ]

    youtube_angle = (
        "Walk through the actual task management practice: how stale items get triaged into ship, kill, or content. "
        "Show the dashboard. Make the case for transparency in agency operations as a trust signal."
    )

    return {
        "id": f"stale-{item.get('id')}",
        "type": "stale_opportunity",
        "weight": days,
        "title": title,
        "hook": hook,
        "reel_outline": reel_outline,
        "youtube_angle": youtube_angle,
        "why_now": f"Action item created {item.get('created_date')}, carried {days} days.",
        "data_pull": f"action_items row #{item.get('id')}",
        "examples": None,
        "sources": [],
        "delivery_cues": [
            f'// Drop on "{days} days." No drama, just the number.',
        ],
    }


# ── Main ─────────────────────────────────────────────────────────────


def rows(cur, sql):
    cur.execute(sql)
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def main():
    if not BRIDGE_DB.exists():
        raise SystemExit(f"bridge.db not found at {BRIDGE_DB}")
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(f"file:{BRIDGE_DB}?mode=ro", uri=True)
    cur = conn.cursor()

    prospects = rows(cur, "SELECT * FROM prospects")
    competitor_activity = rows(cur, """
        SELECT * FROM competitor_activity
        WHERE date >= date('now', '-30 days')
        ORDER BY
          CASE upper(coalesce(threat_level, '')) WHEN 'HIGH' THEN 0 WHEN 'MEDIUM' THEN 1 ELSE 2 END,
          date DESC
        LIMIT 12
    """)
    leads = rows(cur, """
        SELECT * FROM cntemup_leads
        WHERE (suggested_response IS NOT NULL AND length(suggested_response) > 30)
           OR upper(coalesce(urgency, '')) = 'HOT'
        ORDER BY found_date DESC
        LIMIT 15
    """)
    action_items = rows(cur, """
        SELECT * FROM action_items
        WHERE status = 'open' AND coalesce(carried_days, 0) >= 7
        ORDER BY carried_days DESC
        LIMIT 8
    """)

    # Keyword candidates: top movers with at least 2 data points
    kw_raw = rows(cur, """
        SELECT date, site, keyword, position FROM keyword_history ORDER BY keyword, site, date
    """)
    series = {}
    for r in kw_raw:
        key = (r["site"], r["keyword"])
        series.setdefault(key, []).append(r)

    keyword_movers = []
    for (site, keyword), pts in series.items():
        ranked = [p for p in pts if p["position"] is not None]
        if len(ranked) < 2:
            continue
        first, last = ranked[0]["position"], ranked[-1]["position"]
        delta = first - last  # positive = climbed (lower number = better)
        if abs(delta) < 2:
            continue
        keyword_movers.append({
            "keyword": keyword, "site": site,
            "first_position": first, "latest_position": last, "delta": delta,
        })
    keyword_movers.sort(key=lambda k: abs(k["delta"]), reverse=True)

    conn.close()

    # ── Generate briefs ──
    briefs = []

    # 1. Audit pattern briefs
    mined = mine_gaps(prospects)
    for label, count in mined["counts"].most_common(5):
        if count >= 3:  # only patterns hit on 3+ prospects
            briefs.append(brief_audit_pattern(label, count, mined["total"], mined["samples"][label]))

    # 2. Competitor counter briefs (top 5 by threat × recency)
    seen_agencies = set()
    for row in competitor_activity:
        agency = row.get("agency_name")
        if not agency or agency in seen_agencies:
            continue
        seen_agencies.add(agency)
        briefs.append(brief_competitor_counter(row))
        if len(seen_agencies) >= 5:
            break

    # 3. Keyword movement briefs (top 4)
    for kw in keyword_movers[:4]:
        briefs.append(brief_keyword_movement(kw))

    # 4. Reddit response briefs (top 6)
    for lead in leads[:6]:
        b = brief_reddit_response(lead)
        if b:
            briefs.append(b)

    # 5. Stale opportunity briefs (top 3)
    for item in action_items[:3]:
        b = brief_stale_opportunity(item)
        if b:
            briefs.append(b)

    # Sort by weight desc — most actionable at the top
    briefs.sort(key=lambda b: b.get("weight", 0), reverse=True)

    # Add generation metadata
    out = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "voice_lock": "Tom Scott + Johnny Harris + Morgan Housel hybrid (project_content_voice_hybrid.md)",
        "format": "Hook (1-2 sentences) + reel outline (> mandatory, o optional, * land) + YouTube angle (expand never repeat) + sources",
        "counts": {
            "total": len(briefs),
            "by_type": dict(Counter(b["type"] for b in briefs)),
        },
        "briefs": briefs,
    }
    OUT_FILE.write_text(json.dumps(out, indent=2, default=str))
    print(f"Wrote {len(briefs)} briefs to {OUT_FILE}")
    print(f"  by type: {out['counts']['by_type']}")


if __name__ == "__main__":
    main()
