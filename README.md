# NCM integration skill

A [Claude Code](https://code.claude.com) skill for integrating the
**Nepal Can Move (NCM)** courier API into an e-commerce or order-management
project: parcel creation, delivery rates, branches, COD, webhooks and webhook
registration, status sync, returns, refunds, redirects, pickup tickets, labels,
comments and reconciliation. It follows NCM's API documentation v2.

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
| `references/api-contract.md` | Every documented NCM endpoint, errors, limits, synthetic examples, changes from the previous API doc |
| `references/webhooks-and-statuses.md` | Webhook contract, status vocabulary, mapping template, processing and reconciliation rules |
| `references/checklists.md` | Decisions to settle first, implementation order with checkpoints, testing checklist |
| `references/production-lessons.md` | What a live integration did, what broke, and what not to copy |
| `references/open-questions.md` | Questions NCM's documents leave open, with a status per question and NCM's answers as they arrive |
| `docs/ncm-integration-reference.md` | All of the above as one document, plus the breaking changes, a capability matrix, a recommended flow and the discrepancies in NCM's docs |

## Caveats

- Based on NCM's API documentation v2 (file `NCM API DOC V2.pdf`) and webhook
  documentation v1.1 (September 2026, marked beta). NCM's PDFs aren't included.
- "v2" is the document's version, not a URL prefix: create, detail, status,
  comments and rates are still under `/api/v1/`. Code written against the previous API document (file
  dated `251222`) needs two changes, both to tickets; see
  [Changes from the v1 doc](skills/ncm-integration/references/api-contract.md#changes-from-the-v1-doc).
  Guidance kept only from that older document is labelled `[v1 doc]`.
- Nothing was checked against NCM's live API. Claims are labelled `[doc]`,
  `[v1 doc]`, `[inferred]`, `[observed]`, `[reported]`, `[recommended]`,
  `[unknown]` or `[NCM, date]`. Confirm anything labelled `[v1 doc]`,
  `[inferred]`, `[observed]`, `[reported]` or `[unknown]` with NCM or a demo
  token before depending on it.
- Not affiliated with Nepal Can Move.

## Open questions for NCM

NCM's documents leave 24 things unspecified that an integration depends on:
cancellation, rate-limit scope, the comment webhook, branch ids, label barcodes
and more. They're tracked in
[`skills/ncm-integration/references/open-questions.md`](skills/ncm-integration/references/open-questions.md).
When NCM answers one, record it there, update the sections that cite it, and
rebuild the reference (below).

## Editing

Edit the files under `skills/ncm-integration/references/` (and
`docs/src/intro.md` for the reference's introduction), then rebuild the
single-file reference:

```bash
python3 scripts/build_reference.py
```

## License

MIT
