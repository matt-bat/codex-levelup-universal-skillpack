---
name: help
description: Explain the installed Agent Command Center skillpack when the user sends --help, including every active skill, activation marker, supported command, and concise behavior description. Also supplies the exact one-line startup hint required when the pack is first loaded into a conversation; do not activate for unrelated help requests.
---

# Help

## Startup Hint

When the pack is first loaded in a new or existing conversation, print this exact line once:

`send --help to learn more about available tools in agent-command-center`

Do not repeat it every turn. The host instruction file owns startup enforcement because a skill cannot independently observe installation or conversation lifecycle events. When the host can execute local adapters, use `scripts/runtime_adapter.py` and preserve its returned conversation state. Read [Host Runtime Protocol](references/runtime-protocol.md) before integrating or testing a host.

## `--help` Workflow

When the user sends exact command `--help`:

1. Read `skills/skill-catalog.json` when it is available. Treat it as the canonical inventory and routing source.
2. List every skill whose status is `active`. Include deprecated compatibility names in a separate note only when useful.
3. Prefix a skill name with `*` exactly when its catalog `routing_mode` is `explicit_only`.
4. Do not prefix automatic or safety-routed skills. Explain that they trigger when their typed conditions apply.
5. For each skill, use the catalog description or a faithful one-line condensation.
6. Show supported user commands and mode persistence.
7. Keep the result readable: group automatic/safety skills separately from explicit skills when the inventory is long.

If the catalog is unavailable, enumerate installed skill folders containing `SKILL.md`, read their frontmatter, and mark only skills whose metadata explicitly says user activation is required. State that marker accuracy could not be verified against the catalog.

## Marker Legend

- `* skill-name`: requires direct user invocation or enabling.
- `skill-name`: selected automatically by typed task conditions or mandatory safety routing.

The star describes activation, not quality, risk, or installation status.

## Supported Commands

Always include commands that exist in the installed pack:

- `--help`: show this inventory and command guide.
- `--quizme`: toggle exhaustive conversation-local clarification.
- `--quizme --mc`: prefer multiple-choice clarification.
- `--quizme --one-at-a-time`: ask one adaptive question per round.
- `--quizme --confirm`: require confirmation of the final task contract.
- `--quizme --record`: record the approved contract when a suitable artifact is authorized; implies confirmation.
- `--internal-lang on|off`: toggle private compact notation.
- `--internal-lang --response on|off`: toggle compact user-facing notation separately.
- `--clean-slate`: enable the fresh-context boundary.
- `--clean-slate off`: disable the fresh-context boundary.
- `--ill-run-scripts`: toggle the user-run-scripts pause; its state persists across conversations.

Do not advertise a command whose corresponding installed skill or host policy is absent.

## Runtime Conformance

Use `scripts/runtime_adapter.py` as the executable reference for startup, exact-command parsing, and persisted mode transitions. It emits a message digest and a router-ready descriptor patch while atomically storing only explicit mode booleans in the host preference file. A host may implement an equivalent adapter, but must pass the conformance tests and must not claim support from prose-only behavior.

## Output Contract

Return:

1. marker legend
2. complete active-skill inventory
3. supported commands and short descriptions
4. a note that skill activation never grants write, commit, push, publish, deploy, delete, message, or other external authority

Do not create or update any file merely because help was requested.
