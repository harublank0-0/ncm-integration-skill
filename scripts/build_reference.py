"""Build docs/ncm-integration-reference.md from the skill's reference files.

Run from the repository root: python3 scripts/build_reference.py
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REFS = ROOT / "skills" / "ncm-integration" / "references"
PARTS = [
    ("api-contract.md", "API contract"),
    ("webhooks-and-statuses.md", "Webhooks, statuses and status processing"),
    ("checklists.md", "Decisions, implementation and testing checklists"),
    ("production-lessons.md", "Lessons from a production integration"),
]


def demote(text: str) -> str:
    """Push every heading one level down and point sibling links at the skill."""
    text = re.sub(r"^(#+) ", lambda m: "#" + m.group(1) + " ", text, flags=re.M)
    return re.sub(
        r"\]\(((?:api-contract|webhooks-and-statuses|checklists|production-lessons)\.md)",
        r"](../skills/ncm-integration/references/\1",
        text,
    )


def main() -> None:
    out = [(ROOT / "docs" / "src" / "intro.md").read_text().rstrip(), ""]
    for name, title in PARTS:
        body = (REFS / name).read_text()
        body = re.sub(r"\A# .*\n", "", body).strip()
        out += [f"## {title}", "", f"*Source: `skills/ncm-integration/references/{name}`*", "", demote(body), ""]
    (ROOT / "docs" / "ncm-integration-reference.md").write_text("\n".join(out))


if __name__ == "__main__":
    main()
