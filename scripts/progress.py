#!/usr/bin/env python3
from pathlib import Path
import re

path = Path(__file__).resolve().parents[1] / "knowledge" / "progress.yaml"
text = path.read_text(encoding="utf-8")
blocks = re.split(r"\n  - subject: ", text)[1:]
records = []
for raw in blocks:
    block = "subject: " + raw
    def field(name):
        m = re.search(rf"^\s*{re.escape(name)}:\s*(.+?)\s*$", block, re.M)
        return m.group(1).strip().strip('"') if m else None
    level = field("level")
    records.append({
        "subject": field("subject"),
        "topic": field("topic"),
        "type": field("type"),
        "curriculum_id": field("curriculum_id"),
        "level": int(level) if level and level.isdigit() else None,
    })

unique_program = {int(r["curriculum_id"]) for r in records if r["curriculum_id"]}
base = [r for r in records if r["type"] == "base"]
deep = [r for r in records if r["type"] == "deepening"]
independent = [r for r in records if r["level"] is not None and r["level"] >= 3]

print(f"Официальные темы, которых уже касались: {len(unique_program)} / 230")
print(f"Записей фундамента: {len(base)}")
print(f"Записей углубления: {len(deep)}")
print(f"Записей уровня 3+ (самостоятельно или устойчивее): {len(independent)}")
print()
print("Официальные ID:", ", ".join(map(str, sorted(unique_program))))
print()
for subject in sorted({r['subject'] for r in records if r['subject']}):
    subset = [r for r in records if r['subject'] == subject]
    ids = sorted({int(r['curriculum_id']) for r in subset if r['curriculum_id']})
    print(f"{subject}: {len(subset)} записей", end="")
    if ids:
        print(f"; темы программы: {', '.join(map(str, ids))}")
    else:
        print()
