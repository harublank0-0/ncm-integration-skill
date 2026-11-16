# Open questions for NCM

What NCM's documents (API doc v2, webhook doc v1.1) leave unspecified and an
integration depends on. Ask NCM before go-live, and record each answer here.
Background for each question is in [api-contract.md](api-contract.md) and
[webhooks-and-statuses.md](webhooks-and-statuses.md), where the gap is marked
`[unknown]`.

## How to resolve one

1. Set its status to `Answered` and add an entry under [Answers](#answers): the date, who answered and how (for example "NCM IT, by email"), and the answer, quoted where you can.
2. Update every section that cites the gap. Change its `[unknown]` label to `[doc]` if NCM published the answer in a document (add the document to the sources), or to `[NCM, <date>]` if it came by email, call or ticket.
3. Rebuild the single-file reference: `python3 scripts/build_reference.py`.

An answer seen on the live API but not given by NCM is labelled
`[observed <date>]`, never `[doc]` or `[NCM, <date>]`, and its status says
"(observed)". Still ask NCM to confirm it: what one account saw on one day can
change.

Statuses: `Open` (not asked yet), `Asked` (sent to NCM, no answer), `Answered`,
`Partly answered` (some of the question is settled; the rest is still open),
`Dropped` (NCM declined, or it no longer matters; say why under Answers).

## Questions

| # | Topic | Question | Status |
|---|---|---|---|
| 1 | Hosts | The production base URL, and whether demo tokens and data are separate from production. | Partly answered (observed) |
| 2 | Limits | Rate-limit scope (per token?), reset time, the response when it's exceeded, and which endpoints count against the 20,000 daily reads (bulk status, labels, customers, ratings, tickets). | Open |
| 3 | Branches | Response shapes for `/api/v2/branches` and `/api/v1/shipping-rate`, and whether the branch list needs a token. | Answered (observed) |
| 4 | Cancellation | How to cancel an order, or hold one, after create, and whether a ticket type is meant for it. | Open |
| 5 | Cancellation | Whether a parcel can still be collected after you decide to cancel it, and how to stop that. | Open |
| 6 | Status | Maximum batch size for `/api/v1/orders/statuses`, and why an id lands in `errors`. | Partly answered (observed) |
| 7 | COD | What `payment_status` values exist, how COD remittance to the vendor is reported, and what follows a COD transfer ticket. | Partly answered (observed) |
| 8 | Orders | Whether `vref_id` is checked for duplicates, and whether a parcel can be looked up by it (the label's `vendor_orderid` suggests NCM stores it). | Open |
| 9 | Tickets | Whether the v1 doc's ticket path `/api/v2/vendor/ticket/create` still works, and until when. | Open |
| 10 | Tickets | For `Pickup` tickets: whether `branch` is matched case-sensitively, the error for a missing or unassigned branch, and whether create's `fbranch` must also be an assigned pickup branch. | Open |
| 11 | Tickets | Which ticket-detail `status` value means open. | Open |
| 12 | Webhooks | How to set an order comment webhook URL through the API (the webhook endpoint mentions comment events and "URLs" but takes only `webhook_url`), and the comment event's payload. | Open |
| 13 | Webhooks | The full list of order statuses and webhook events, including `comment_added`, `returned_to_warehouse`, and the maximum ids in one bulk event. | Open |
| 14 | Orders | Whether undocumented fields (`vendor_return`, `delivered_date`, `active`, a tracking id) and `/order/redirectable` are supported for vendors. | Partly answered (observed) |
| 15 | Webhooks | Whether webhooks for one parcel arrive in order. | Open |
| 16 | Orders | Which characters names and addresses may contain (Devanagari?), and the length limits per field, comment and ticket response. | Open |
| 17 | Webhooks | How to rotate a webhook secret without losing events: whether a new `webhook_url` takes effect at once, and whether the old one keeps receiving in-flight events. | Open |
| 18 | COD | Whether `cod_charge: "0"` is accepted for a prepaid order, and what the rider then collects. | Open |
| 19 | Branches | Where branch ids come from, since the redirect's `destination` needs one, and whether the label's branch `code` is accepted anywhere. | Partly answered (observed) |
| 20 | Status | Whether `Delivery Attempted`, `Out for Delivery` and `Dispatched to <BRANCH>` are real status strings, and what `returned_to_warehouse` means. | Open |
| 21 | Comments | Whether posting a comment or a ticket response is idempotent in any way, since a comment returns no id. | Open |
| 22 | Customers | Whether customer detail's `orders` covers only your account, and the terms for using rating stats, which describe other vendors' orders. | Open |
| 23 | Labels | What a barcode should encode, whether a printable label exists, how to set `handling` at create, and which orders have a non-vendor `from`. | Open |
| 24 | Webhooks | Whether test webhooks carry the same headers as real ones. | Open |

## Answers

Entries dated 2026-11-16 come from read-only calls to the production API with
one vendor's production token (23 calls, shapes only; see the sources in
[api-contract.md](api-contract.md)). None is confirmed by NCM; ask NCM to
confirm each before go-live.

### 1. Hosts
2026-11-16, observed with the production token via read-only calls; not
confirmed by NCM. `https://portal.nepalcanmove.com` is the production host. It
takes the same `Authorization: Token <token>` header as the demo examples. The
account holder reports that demo and production tokens are separate [reported].
Still open: whether the demo shares any data with production.
Updated: api-contract.md (Basics: Host, Sandbox), SKILL.md.

### 3. Branch list and rate shapes
2026-11-16, observed with the production token via read-only calls; not
confirmed by NCM.
- `GET /api/v2/branches` returns one bare JSON array of every branch, not paged (649 that day). Items: `pk` (integer), `code`, `name`, `geocode`, `address`, `surcharge` (decimal string, can be negative), `phone`, `phone2`, `branch_type` (`Branch` or `Logistics`), `areas_covered` (one string), `province_name`, `district_name`. `geocode`, `address`, `areas_covered` and `phone2` can be `null`.
- It answers without a token, with the same list.
- `GET /api/v1/shipping-rate` returns `{"charge": "<decimal string>"}`. Only branch names work: a branch's `code` or `pk`, or an unknown name, gets HTTP 200 with an HTML error page. An unknown `type` gets `200 {"charge": "0"}`.

Updated: api-contract.md (Basics, Errors, endpoint catalog #1 and #2, Delivery
types, Branches and rates), SKILL.md.

### 6. Bulk status
2026-11-16, observed with the production token via read-only calls; not
confirmed by NCM. An id that doesn't exist is listed in `errors` as an integer,
while a known id in the same call is answered in `result`. Still open: the
maximum batch size, and other causes of an `errors` entry.
Updated: api-contract.md (endpoint catalog #9, Status history and bulk status).

### 7. COD and payment_status
2026-11-16, observed with the production token via read-only calls; not
confirmed by NCM. An undelivered parcel read `payment_status: "Delivery
Pending"`; the doc shows `"Completed"`. Still open: the full list of values,
what each means, how remittance is reported, and what follows a COD ticket.
Updated: api-contract.md (Order detail).

### 14. Undocumented order fields
2026-11-16, observed with the production token via read-only calls; not
confirmed by NCM. The production order detail carries `vendor_return` (the
**string** `"False"`, not a boolean), `trackid` (a string), `active` (a
boolean), `delivered_date` (`null` before delivery), and two more:
`destination_branch_name` and `destination_branch_phone`. Each status-history
row also carries `vendor_return`. Still open: whether vendors may rely on these
fields, and `/order/redirectable`, which wasn't called.
Updated: api-contract.md (endpoint catalog #3 and #6, Order detail, Status
history and bulk status), SKILL.md.

### 19. Branch ids
2026-11-16, observed with the production token via read-only calls; not
confirmed by NCM. The branch list carries an integer `pk` and a `code` for each
branch. The rate endpoint accepts neither: it takes names only. Still open:
whether the redirect's `destination` takes the branch `pk` (redirect wasn't
called), and whether the label's `code` is accepted anywhere.
Updated: api-contract.md (Branches and rates, Redirect).

Format for an answer NCM gives:

```text
### 9. Old ticket path
2026-12-01, NCM IT, by email: "<answer>"
Updated: api-contract.md (Changes from the v1 doc, Tickets).
```
