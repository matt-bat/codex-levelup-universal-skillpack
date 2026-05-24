# Cache Budgets

One-line overview: Default caps for cached summaries, indexes, and compact metadata files.

| Artifact | Max Active Entries | Max Summary Length | Max Notes Length | Prune Rule |
|---|---:|---:|---:|---|
| `docs/chat-history-summary.md` | 10 | 60 words | 20 words | Remove oldest low-value entry |
| `docs/chat-history-index.md` | 30 | 40 words | 25 words | Merge duplicates, then trim oldest superseded entries |
| `user-instructions.md` | 80 rows | 30 words | 25 words | Consolidate stale or superseded rows where possible |
| Compact tracker tables | 50 rows | 40 words | 20 words | Prefer canonical file of record and prune duplicates |

Notes:
- A repo-specific file may define a stricter cap.
- When caps conflict, use the stricter rule.
- Preserve the newest accurate state over older cached variants.
