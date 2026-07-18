# Notation and Safety

Use this reference only after `internal-lang` has been explicitly activated and compact notation will be emitted or interpreted.

## Notation

| Token | Meaning |
|---|---|
| `G` | goal |
| `R` | requirement |
| `C` | constraint |
| `A` | assumption |
| `Q` | question |
| `D` | decision |
| `E` | evidence |
| `V` | validation |
| `B` | blocker |
| `N` | note |
| `T` | task |
| `S` | state |
| `F` | follow-up |
| `!` | risk |
| `?` | uncertainty |
| `->` | leads to |
| `=>` | result |
| `x` | blocked by |
| `ok` | verified or accepted |

Example:

```text
G: add toggle
R: normal response unless response mode is on
!: preserve user requirements exactly
V: command-state checks
```

## Compression Gate

Compress only when all are true:
1. a future reader can restore the meaning without asking the user
2. the full-fidelity source remains available
3. the content is low-risk and non-action-critical
4. compression produces a meaningful reduction

Otherwise, use normal language.

## Expansion Test

Before compact content influences implementation, validation, or handoff:
1. expand every symbol into plain language
2. preserve every requirement, constraint, risk, and blocker
3. remove the compact version if expansion changes or weakens meaning

## Durable Artifacts

Do not place shorthand in commits, documentation, issue comments, or other durable artifacts unless the user explicitly requested compact notation there. When durable shorthand is requested, include a plain-language key and expand all consequential content.
