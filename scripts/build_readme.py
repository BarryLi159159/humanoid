#!/usr/bin/env python3
"""Build README.md from data/*.yaml.

Usage: python scripts/build_readme.py
Each data file holds one or more (topicN, papersN) pairs. Paper fields:
  id        arXiv id (YYMM.NNNNN) or a slug when no arXiv id exists
  link      optional; defaults to https://arxiv.org/abs/<id>
  date      optional "YYYY.MM"; derived from the arXiv id when omitted
  name, title, venue, novelty, limitation
  depth     A = curated from abstract/paper, T = title/list-level only
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ARXIV_RE = re.compile(r"^(\d{2})(\d{2})\.\d{4,5}$")
REQUIRED = ["id", "name", "title", "venue", "novelty", "limitation", "depth"]


def load_papers():
    by_topic, seen, errors = {}, {}, []
    for f in sorted(DATA.glob("*.yaml")):
        if f.name == "topics.yaml":
            continue
        doc = yaml.safe_load(f.read_text())
        for key, val in doc.items():
            if not key.startswith("topic"):
                continue
            suffix = key[len("topic"):]
            for p in doc.get("papers" + suffix, []):
                missing = [k for k in REQUIRED if not p.get(k)]
                if missing:
                    errors.append(f"{f.name}: {p.get('id')} missing {missing}")
                    continue
                pid = str(p["id"])
                if pid in seen:
                    errors.append(f"duplicate id {pid} in {f.name} and {seen[pid]}")
                seen[pid] = f.name
                m = ARXIV_RE.match(pid)
                if m:
                    p.setdefault("date", f"20{m.group(1)}.{m.group(2)}")
                    p.setdefault("link", f"https://arxiv.org/abs/{pid}")
                elif not (p.get("date") and p.get("link")):
                    errors.append(f"{pid}: non-arXiv entry needs date and link")
                    continue
                if p["date"] < "2025.01":
                    errors.append(f"{pid}: date {p['date']} is before scope (2025.01)")
                by_topic.setdefault(val, []).append(p)
    return by_topic, errors


def cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


def sort_key(p):
    m = ARXIV_RE.match(str(p["id"]))
    num = float(str(p["id"])) if m else 0.0
    return (p["date"], num)


def render(topics, by_topic):
    total = sum(len(v) for v in by_topic.values())
    out = []
    out.append((ROOT / "docs" / "header.md").read_text().rstrip())
    out.append("")
    out.append(f"**{total} papers** · last updated 2026-09-25 · sorted newest first within each topic")
    out.append("")
    out.append("## Contents")
    out.append("")
    for t in topics:
        n = len(by_topic.get(t["key"], []))
        anchor = re.sub(r"[^a-z0-9 -]", "", t["title"].lower()).replace(" ", "-")
        out.append(f"- [{t['title']}](#{anchor}) ({n})")
    out.append("")
    out.append((ROOT / "docs" / "big_picture.md").read_text().rstrip())
    out.append("")
    for t in topics:
        papers = sorted(by_topic.get(t["key"], []), key=sort_key, reverse=True)
        out.append("---")
        out.append("")
        out.append(f"## {t['title']}")
        out.append("")
        out.append(t["summary"].rstrip())
        out.append("")
        out.append("| Date | Paper | Venue | Novelty | Limitation |")
        out.append("|---|---|---|---|---|")
        for p in papers:
            mark = "" if p["depth"] == "A" else " †"
            paper = f"[**{cell(p['name'])}**]({p['link']}){mark}<br><sub>{cell(p['title'])}</sub>"
            out.append(
                f"| {p['date']} | {paper} | {cell(p['venue'])} | {cell(p['novelty'])} | {cell(p['limitation'])} |"
            )
        out.append("")
    out.append("---")
    out.append("")
    out.append((ROOT / "docs" / "footer.md").read_text().rstrip())
    out.append("")
    return "\n".join(out)


def main():
    topics = yaml.safe_load((DATA / "topics.yaml").read_text())
    by_topic, errors = load_papers()
    unknown = set(by_topic) - {t["key"] for t in topics}
    if unknown:
        errors.append(f"unknown topic keys: {unknown}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)
    (ROOT / "README.md").write_text(render(topics, by_topic))
    counts = {t["key"]: len(by_topic.get(t["key"], [])) for t in topics}
    print("README.md written:", counts, "total", sum(counts.values()))


if __name__ == "__main__":
    main()
