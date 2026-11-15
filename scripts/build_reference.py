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
    ("open-questions.md", "Open questions for NCM"),
]


SIBLING_LINK = re.compile(r"\]\((" + "|".join(re.escape(name) for name, _ in PARTS) + r")")


def demote(text: str) -> str:
    """Push every heading one level down and point sibling links at the skill.

    Lines inside fenced code blocks are left alone.
    """
    lines, in_fence = [], False
    for line in text.split("\n"):
        if line.startswith("```"):
            in_fence = not in_fence
        elif not in_fence and re.match(r"#+ ", line):
            line = "#" + line
        lines.append(line)
    return SIBLING_LINK.sub(r"](../skills/ncm-integration/references/\1", "\n".join(lines))


def main() -> None:
    out = [(ROOT / "docs" / "src" / "intro.md").read_text().rstrip(), ""]
    for name, title in PARTS:
        body = (REFS / name).read_text()
        body = re.sub(r"\A# .*\n", "", body).strip()
        out += [f"## {title}", "", f"*Source: `skills/ncm-integration/references/{name}`*", "", demote(body), ""]
    (ROOT / "docs" / "ncm-integration-reference.md").write_text("\n".join(out))


if __name__ == "__main__":
    main()
