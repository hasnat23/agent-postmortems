"""Validate incidents/ and regenerate README.md tables and docs/incidents.json.

    python scripts/build.py           # validate and write
    python scripts/build.py --check   # validate and fail if generated files are stale
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
INCIDENTS = ROOT / "incidents"
SCHEMA = ROOT / "schema" / "incident.schema.json"
README = ROOT / "README.md"
DATA = ROOT / "docs" / "incidents.json"

SEVERITY_BADGE = {"critical": "🟥 critical", "high": "🟧 high", "medium": "🟨 medium", "low": "⬜ low"}


class ValidationError(Exception):
    pass


def load() -> list[dict]:
    validator = Draft202012Validator(json.loads(SCHEMA.read_text()))
    errors: list[str] = []
    incidents: list[dict] = []
    seen_urls: dict[str, str] = {}

    for path in sorted(INCIDENTS.glob("*.yaml")):
        rel = path.relative_to(ROOT).as_posix()
        try:
            # BaseLoader keeps every scalar a string, so dates stay "2025-07".
            doc = yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
        except yaml.YAMLError as exc:
            errors.append(f"{rel}: invalid YAML: {exc}")
            continue
        if not isinstance(doc, dict):
            errors.append(f"{rel}: expected a mapping at the top level")
            continue
        for err in validator.iter_errors(doc):
            where = "/".join(str(p) for p in err.absolute_path) or "(root)"
            errors.append(f"{rel}: {where}: {err.message}")
        if not re.fullmatch(rf"{re.escape(str(doc.get('id')))}-[a-z0-9]+(-[a-z0-9]+)*\.yaml", path.name):
            errors.append(f"{rel}: file name must be '<id>-<kebab-slug>.yaml'")
        for src in doc.get("sources", []) if isinstance(doc.get("sources"), list) else []:
            url = src.get("url") if isinstance(src, dict) else None
            if url and url in seen_urls:
                # One write-up can cover several incidents, so this is only a hint.
                print(f"note: {rel} shares a source with {seen_urls[url]}", file=sys.stderr)
            elif url:
                seen_urls[url] = doc.get("id")
        doc["file"] = rel
        incidents.append(doc)

    ids = [i.get("id") for i in incidents]
    for dup in sorted(k for k, v in Counter(ids).items() if v > 1):
        errors.append(f"duplicate id {dup}")
    expected = [f"AP-{n:04d}" for n in range(1, len(incidents) + 1)]
    if sorted(ids) != expected and not errors:
        missing = sorted(set(expected) - set(ids))
        errors.append(f"ids must be contiguous from AP-0001; missing {', '.join(missing)}")

    if errors:
        raise ValidationError("\n".join(errors))
    return incidents


def render_stats(incidents: list[dict]) -> str:
    total = len(incidents)
    wild = sum(1 for i in incidents if i["status"] == "in-the-wild")
    classes = Counter(c for i in incidents for c in i["classes"])
    years = sorted({i["date"][:4] for i in incidents})
    lines = [
        f"**{total} incidents** from {years[0]} to {years[-1]}: "
        f"**{wild}** hit real users or systems, **{total - wild}** were demonstrated by researchers.",
        "",
        "| Failure class | Incidents | |",
        "|---|---:|---|",
    ]
    top = max(classes.values())
    for name, count in classes.most_common():
        bar = "█" * max(1, round(count / top * 20))
        lines.append(f"| [`{name}`](TAXONOMY.md#{name}) | {count} | `{bar}` |")
    return "\n".join(lines)


def render_table(incidents: list[dict]) -> str:
    lines = ["| ID | Date | Incident | Classes | Severity | Status |", "|---|---|---|---|---|---|"]
    for i in sorted(incidents, key=lambda i: (i["date"], i["id"]), reverse=True):
        title = i["title"].replace("|", "\\|")
        classes = " ".join(f"`{c}`" for c in i["classes"])
        status = "🔥 in the wild" if i["status"] == "in-the-wild" else "🧪 research"
        lines.append(
            f"| [{i['id']}]({i['file']}) | {i['date']} | {title} | {classes} | "
            f"{SEVERITY_BADGE[i['severity']]} | {status} |"
        )
    return "\n".join(lines)


def replace_block(text: str, name: str, body: str) -> str:
    pattern = re.compile(rf"(<!-- BEGIN:{name} -->\n).*?(<!-- END:{name} -->)", re.S)
    if not pattern.search(text):
        raise ValidationError(f"README.md is missing the {name} markers")
    return pattern.sub(lambda m: m.group(1) + body + "\n" + m.group(2), text)


def build(check: bool) -> int:
    try:
        incidents = load()
        readme = README.read_text(encoding="utf-8")
        new_readme = replace_block(readme, "STATS", render_stats(incidents))
        new_readme = replace_block(new_readme, "INCIDENTS", render_table(incidents))
    except ValidationError as exc:
        print(exc, file=sys.stderr)
        return 1

    public = sorted(incidents, key=lambda i: (i["date"], i["id"]), reverse=True)
    new_data = json.dumps(public, indent=2, ensure_ascii=False) + "\n"

    stale = []
    if readme != new_readme:
        stale.append(README)
    if not DATA.exists() or DATA.read_text(encoding="utf-8") != new_data:
        stale.append(DATA)

    if check:
        if stale:
            names = ", ".join(p.relative_to(ROOT).as_posix() for p in stale)
            print(f"Generated files are out of date: {names}. Run `python scripts/build.py`.", file=sys.stderr)
            return 1
        print(f"OK: {len(incidents)} incidents valid, generated files up to date.")
        return 0

    README.write_text(new_readme, encoding="utf-8")
    DATA.parent.mkdir(exist_ok=True)
    DATA.write_text(new_data, encoding="utf-8")
    print(f"Wrote README.md and docs/incidents.json ({len(incidents)} incidents).")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="fail if generated files are stale")
    sys.exit(build(parser.parse_args().check))
