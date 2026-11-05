# NCM integration skill

A [Claude Code](https://code.claude.com) skill for integrating the
**Nepal Can Move (NCM)** courier API into an e-commerce or order-management
project: parcel creation, delivery rates, branches, COD, webhooks, status sync,
returns, refunds, redirects, tickets, comments and reconciliation.

It separates what NCM's documents actually say from what one production
integration learned the hard way, and it makes Claude settle the business
decisions (cancellation, returns, COD settlement, stock) with you instead of
guessing. It assumes no particular framework.

## Install

As a plugin (updates with `claude plugin update`):

```bash
claude plugin marketplace add harublank0-0/ncm-integration-skill
```

```bash
claude plugin install ncm-integration@ncm-integration-skill
```

Or copy the skill into a project:

```bash
git clone https://github.com/harublank0-0/ncm-integration-skill && mkdir -p .claude/skills && cp -R ncm-integration-skill/skills/ncm-integration .claude/skills/
```

Then ask Claude to add or fix an NCM integration; the skill loads when the task
mentions NCM or Nepal Can Move.

## What's inside

| Path | Contents |
|---|---|
| `skills/ncm-integration/SKILL.md` | When to use it, what to inspect first, the workflow, common mistakes |
| `references/api-contract.md` | Every documented NCM endpoint, errors, limits, synthetic examples, open questions for NCM |
| `references/webhooks-and-statuses.md` | Webhook contract, status vocabulary, mapping template, processing and reconciliation rules |
| `references/checklists.md` | Decisions to settle first, implementation order with checkpoints, testing checklist |
| `references/production-lessons.md` | What a live integration did, what broke, and what not to copy |
| `docs/ncm-integration-reference.md` | All of the above as one document, plus a capability matrix, a recommended flow and the discrepancies in NCM's docs |

## Caveats

- Based on NCM's API documentation (file dated `251222`) and webhook
  documentation v1.1 (September 2026, marked beta). NCM's PDFs aren't included.
- Nothing was checked against NCM's live API. Claims are labelled `[doc]`,
  `[inferred]`, `[observed]`, `[reported]` or `[unknown]`; confirm the last four
  with NCM or a demo token.
- Not affiliated with Nepal Can Move.

## Editing

Edit the files under `skills/ncm-integration/references/`, then rebuild the
single-file reference:

```bash
python3 scripts/build_reference.py
```

## License

MIT
