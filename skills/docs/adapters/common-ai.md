# Common AI Instructions

[Documentation home](../README.md) · [Install profiles](../install-profiles.md) · [Usage](../../USAGE.md)

Use this repository with ChatGPT, Claude, Gemini, Cursor, GitHub Copilot, or any assistant that can read markdown files and follow local project instructions.

## Fast Setup

1. put the repository in the assistant's workspace
2. load the root `AGENTS.md`
3. load `skills/skill-catalog.json` or its generated decision-tree view
4. load only the skill files selected for the task
5. request a skill declaration only when you need one explicitly or when governed/audited work needs a durable routing record
6. keep the repo's instruction files visible in the workspace for the whole task
7. when local script execution is available, use `skills/help/scripts/runtime_adapter.py` for startup and exact-command state; otherwise implement and test the same protocol described in `skills/help/references/runtime-protocol.md`, including durable preference persistence when a writable path exists
8. after installing or updating, run the post-install validation commands in `skills/docs/install-profiles.md`

## Project Instructions

If the assistant supports project instructions or custom workspace rules, paste a short summary there:

```md
Use the repository instructions and the active skill docs in this repo. Route by requested action and planned effect, allow a zero-skill route for routine work, and declare selected skills only when explicitly requested or when governed/audited work needs a durable routing record.
```

## Common Tooling Patterns

Different assistants expose different controls, but the workflow is the same:

1. `ChatGPT`: use a project or workspace with the repo files attached
2. `Claude`: attach the repo files to the project context or custom instructions
3. `Gemini`: provide the repo files in the workspace and point the model to `AGENTS.md`
4. `Cursor`: keep the repository open and let workspace rules read from the repo root
5. `GitHub Copilot`: keep the repo open in the editor and point it at the root instruction files

The canonical catalog uses schema v2 and declares router contract 2.1. New governed artifacts use governance schema v3; schema-v1 and schema-v2 artifacts remain historical compatibility inputs. If remote publication is authorized and `main` is protected, use a feature branch and pull request so required checks run.

When normalizing task intent, set `action.approach_state` from evidence rather than tone: use `viable` for a routine first error, `challenged` when a material observation or correction undermines the method, and `failed` after the method no longer has an evidence-backed next step. Challenged and failed states select `agent-humility`; the skill does not grant permission to retry commands, edit files, or broaden scope.

## Quizme Mode

If the assistant understands `--quizme`, use it for exhaustive clarification before substantive work.
If it does not, use the assistant's closest equivalent to stop and clarify before it starts editing or running risky commands.

Do not claim lifecycle-command conformance merely because the instruction text was loaded. Conformance requires the reference adapter tests or equivalent host-level tests.
