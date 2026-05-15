#!/usr/bin/env python3
"""
Export bridge.db + markdown digests into JSON files for the dashboard.

Reads:
  ~/Documents/CNTEMUP/claude-bridge/data/bridge.db
  ~/Documents/CNTEMUP/claude-bridge/daily-digest/compiled/*.md

Writes to seamlessflow-site/data/:
  summary.json, prospects.json, competitors.json, competitor_activity.json,
  keywords.json, action_items.json, cntemup_leads.json, outreach.json,
  content_ideas.json, suggestions.json, audits.json
"""

import json
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

HOME = Path.home()
BRIDGE_DB = HOME / "Documents/CNTEMUP/claude-bridge/data/bridge.db"
DIGEST_DIR = HOME / "Documents/CNTEMUP/claude-bridge/daily-digest"
OUT_DIR = HOME / "Documents/SeamLessFlow/seamlessflow-site/data"


def rows(cur, sql, params=()):
    cur.execute(sql, params)
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def write_json(name, data):
    path = OUT_DIR / name
    path.write_text(json.dumps(data, indent=2, default=str))
    size_kb = path.stat().st_size / 1024
    print(f"  {name}: {len(data) if isinstance(data, list) else 'object'} rows, {size_kb:.1f} KB")


def export_prospects(cur):
    data = rows(cur, """
        SELECT id, found_date, business_name, location, website,
               seo_score, outreach_angle, status, last_contact_date,
               qualification_score, fed_to_crm
        FROM prospects
        ORDER BY
          CASE WHEN qualification_score IS NULL THEN 1 ELSE 0 END,
          qualification_score DESC,
          found_date DESC
    """)
    return data


def export_competitors(cur):
    # Roll up activity per agency: total activity, latest threat level, last seen
    data = rows(cur, """
        SELECT
          agency_name,
          COUNT(*) AS activity_count,
          MAX(date) AS last_seen,
          MIN(date) AS first_seen,
          (SELECT threat_level FROM competitor_activity ca2
           WHERE ca2.agency_name = ca1.agency_name
           ORDER BY date DESC LIMIT 1) AS latest_threat_level,
          (SELECT detail FROM competitor_activity ca2
           WHERE ca2.agency_name = ca1.agency_name
           ORDER BY date DESC LIMIT 1) AS latest_detail,
          (SELECT activity_type FROM competitor_activity ca2
           WHERE ca2.agency_name = ca1.agency_name
           ORDER BY date DESC LIMIT 1) AS latest_activity_type
        FROM competitor_activity ca1
        GROUP BY agency_name
        ORDER BY
          CASE latest_threat_level WHEN 'HIGH' THEN 0 WHEN 'high' THEN 0
                                   WHEN 'MEDIUM' THEN 1 WHEN 'medium' THEN 1
                                   ELSE 2 END,
          last_seen DESC
    """)
    return data


def export_competitor_activity(cur):
    # Recent activity feed (last 90 days)
    cutoff = (datetime.now() - timedelta(days=90)).date().isoformat()
    data = rows(cur, """
        SELECT date, agency_name, threat_level, activity_type, detail, source_url
        FROM competitor_activity
        WHERE date >= ?
        ORDER BY date DESC
    """, (cutoff,))
    return data


def export_keywords(cur):
    # Group by keyword/site, build date series for charting
    raw = rows(cur, """
        SELECT date, site, keyword, position, url
        FROM keyword_history
        ORDER BY keyword, site, date
    """)

    series = defaultdict(lambda: {"site": "", "keyword": "", "points": []})
    for r in raw:
        key = f"{r['site']}|{r['keyword']}"
        series[key]["site"] = r["site"]
        series[key]["keyword"] = r["keyword"]
        series[key]["points"].append({
            "date": r["date"],
            "position": r["position"],
            "url": r["url"],
        })

    # Compute deltas vs first observation per keyword
    result = []
    for key, s in series.items():
        points = s["points"]
        first = next((p["position"] for p in points if p["position"] is not None), None)
        last = next((p["position"] for p in reversed(points) if p["position"] is not None), None)
        in_top10_now = last is not None and last <= 10
        in_top10_ever = any(p["position"] is not None and p["position"] <= 10 for p in points)
        result.append({
            "site": s["site"],
            "keyword": s["keyword"],
            "first_position": first,
            "latest_position": last,
            "delta": (first - last) if (first is not None and last is not None) else None,
            "in_top10_now": in_top10_now,
            "in_top10_ever": in_top10_ever,
            "points": points,
        })

    # Sort: top-10 first, then by absolute delta
    result.sort(key=lambda x: (
        0 if x["in_top10_now"] else (1 if x["in_top10_ever"] else 2),
        -(abs(x["delta"]) if x["delta"] is not None else -1),
    ))
    return result


def export_action_items(cur):
    data = rows(cur, """
        SELECT id, created_date, content, status, carried_days
        FROM action_items
        ORDER BY
          CASE status WHEN 'open' THEN 0 ELSE 1 END,
          carried_days DESC,
          created_date DESC
    """)
    return data


def export_cntemup_leads(cur):
    data = rows(cur, """
        SELECT id, found_date, platform, post_url, user_handle, post_text,
               suggested_response, region, urgency
        FROM cntemup_leads
        ORDER BY
          CASE urgency WHEN 'hot' THEN 0 WHEN 'warm' THEN 1 ELSE 2 END,
          found_date DESC
    """)
    return data


def export_outreach(cur):
    data = rows(cur, """
        SELECT ol.id, ol.draft_date, ol.channel, ol.draft_path, ol.status, ol.sent_date, ol.notes,
               p.business_name, p.qualification_score, p.location
        FROM outreach_log ol
        LEFT JOIN prospects p ON ol.prospect_id = p.id
        ORDER BY ol.draft_date DESC
    """)
    return data


def export_suggestions(cur):
    data = rows(cur, """
        SELECT id, date, source_task, category, suggestion, evidence, priority, status, result_notes
        FROM suggestions
        ORDER BY date DESC
        LIMIT 200
    """)
    return data


def export_audits(cur):
    data = rows(cur, """
        SELECT id, check_date, client_name, audit_url, last_commit, days_old, status
        FROM audit_checks
        ORDER BY check_date DESC
    """)
    return data


_MD_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")


def extract_links(*texts):
    """Pull all markdown-style [label](url) pairs out of the given texts, deduped by URL."""
    seen = {}
    for t in texts:
        if not t:
            continue
        for label, url in _MD_LINK_RE.findall(t):
            if url not in seen:
                seen[url] = label.strip()
    return [{"label": v, "url": k} for k, v in seen.items()]


def strip_markdown_links(text):
    """Replace [label](url) with just label so display text reads cleanly."""
    if not text:
        return text
    return _MD_LINK_RE.sub(r"\1", text)


def parse_content_ideas():
    """Parse compiled weekly content-ideas markdown into structured rows."""
    pattern_dir = DIGEST_DIR / "compiled"
    if not pattern_dir.exists():
        return []

    ideas = []
    for path in sorted(pattern_dir.glob("week-*-content-ideas.md")):
        text = path.read_text()
        # Extract week date from filename: week-2026-05-06-content-ideas.md
        m = re.match(r"week-(\d{4}-\d{2}-\d{2})", path.name)
        week_of = m.group(1) if m else None

        # Split into CNTEMUP / SeamlessFlow sections
        sections = {}
        for hdr in re.finditer(r"^## ([A-Za-z]+) Content Ideas$", text, re.MULTILINE):
            site = hdr.group(1)
            start = hdr.end()
            next_hdr = re.search(r"^## ", text[start:], re.MULTILINE)
            end = start + next_hdr.start() if next_hdr else len(text)
            sections[site] = text[start:end]

        for site, section_text in sections.items():
            # Each idea: "### 1. Title"
            for m in re.finditer(
                r"^### \d+\.\s+(.+?)$"
                r"((?:(?!^### \d+\.).)*?)"
                r"(?=^### \d+\.|\Z)",
                section_text,
                re.MULTILINE | re.DOTALL,
            ):
                title = m.group(1).strip()
                body = m.group(2)
                kw = re.search(r"\*\*Target keyword:\*\*\s*(.+?)$", body, re.MULTILINE)
                diff = re.search(r"\*\*Difficulty:\*\*\s*(.+?)$", body, re.MULTILINE)
                ctype = re.search(r"\*\*Content type:\*\*\s*(.+?)$", body, re.MULTILINE)
                link_from = re.search(r"\*\*Link from:\*\*\s*(.+?)$", body, re.MULTILINE)
                why_now = re.search(r"\*\*Why now:\*\*\s*(.+?)(?=^\s*\*\*|\Z)", body, re.MULTILINE | re.DOTALL)
                outline_match = re.search(r"\*\*Outline:\*\*(.*?)(?=^\s*\*\*|\Z)", body, re.MULTILINE | re.DOTALL)

                why_now_raw = why_now.group(1).strip() if why_now else None
                outline_raw = outline_match.group(1).strip() if outline_match else None

                ideas.append({
                    "week_of": week_of,
                    "site": site,
                    "title": title,
                    "target_keyword": kw.group(1).strip() if kw else None,
                    "difficulty": diff.group(1).strip() if diff else None,
                    "content_type": ctype.group(1).strip() if ctype else None,
                    "link_from": link_from.group(1).strip() if link_from else None,
                    "why_now": strip_markdown_links(why_now_raw),
                    "outline_md": outline_raw,
                    "sources": extract_links(why_now_raw, outline_raw, body),
                    "status": "idea",
                })

    # Dedupe by (site, title) keeping newest week
    seen = {}
    for idea in sorted(ideas, key=lambda x: x.get("week_of") or "", reverse=True):
        key = (idea["site"], idea["title"].lower())
        if key not in seen:
            seen[key] = idea
    return list(seen.values())


def build_summary(prospects, competitors, keywords, action_items, leads, ideas, audits, conn):
    cur = conn.cursor()

    # Latest date in keyword_history (last pipeline run)
    latest_kw = cur.execute("SELECT MAX(date) FROM keyword_history").fetchone()[0]

    # Prospect status distribution
    status_dist = Counter(p["status"] or "new" for p in prospects)

    # Open action items > 5 days
    stale_count = sum(1 for a in action_items if a["status"] == "open" and (a["carried_days"] or 0) > 5)

    # Competitors HIGH threat
    high_threat = sum(1 for c in competitors if (c.get("latest_threat_level") or "").upper() == "HIGH")

    # Hot leads
    hot_leads = sum(1 for l in leads if (l.get("urgency") or "").lower() == "hot")

    # Keywords in top 10
    top10_keywords = sum(1 for k in keywords if k["in_top10_now"])

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "latest_pipeline_run": latest_kw,
        "counts": {
            "prospects": len(prospects),
            "competitors_tracked": len(competitors),
            "keywords_tracked": len(keywords),
            "action_items_total": len(action_items),
            "action_items_open": sum(1 for a in action_items if a["status"] == "open"),
            "action_items_stale": stale_count,
            "cntemup_leads": len(leads),
            "content_ideas": len(ideas),
            "audits": len(audits),
        },
        "highlights": {
            "prospects_by_status": dict(status_dist),
            "high_threat_competitors": high_threat,
            "hot_cntemup_leads": hot_leads,
            "keywords_in_top10": top10_keywords,
        },
    }


def main():
    if not BRIDGE_DB.exists():
        print(f"ERROR: bridge.db not found at {BRIDGE_DB}", file=sys.stderr)
        sys.exit(1)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Reading {BRIDGE_DB}")
    print(f"Writing to {OUT_DIR}")
    print("")

    conn = sqlite3.connect(f"file:{BRIDGE_DB}?mode=ro", uri=True)
    cur = conn.cursor()

    prospects = export_prospects(cur)
    competitors = export_competitors(cur)
    competitor_activity = export_competitor_activity(cur)
    keywords = export_keywords(cur)
    action_items = export_action_items(cur)
    cntemup_leads = export_cntemup_leads(cur)
    outreach = export_outreach(cur)
    suggestions = export_suggestions(cur)
    audits = export_audits(cur)
    content_ideas = parse_content_ideas()

    write_json("prospects.json", prospects)
    write_json("competitors.json", competitors)
    write_json("competitor_activity.json", competitor_activity)
    write_json("keywords.json", keywords)
    write_json("action_items.json", action_items)
    write_json("cntemup_leads.json", cntemup_leads)
    write_json("outreach.json", outreach)
    write_json("suggestions.json", suggestions)
    write_json("audits.json", audits)
    write_json("content_ideas.json", content_ideas)

    summary = build_summary(prospects, competitors, keywords, action_items, cntemup_leads, content_ideas, audits, conn)
    write_json("summary.json", summary)

    conn.close()
    print("")
    print("Done.")


if __name__ == "__main__":
    main()
