# Common AI Instructions

Use this repository with ChatGPT, Claude, Gemini, Cursor, GitHub Copilot, or any assistant that can read markdown files and follow local project instructions.

## Fast Setup

1. put the repository in the assistant's workspace
2. load the root `AGENTS.md`
3. load `skills/skill-catalog.json` or its generated decision-tree view
4. load only the skill files selected for the task
5. request a skill declaration only for governed/audited work or when you need one explicitly
6. keep the repo's instruction files visible in the workspace for the whole task

## Project Instructions

If the assistant supports project instructions or custom workspace rules, paste a short summary there:

```md
Use the repository instructions and the active skill docs in this repo. Route by requested action and planned effect, allow a zero-skill route for routine work, and declare selected skills only for governed/audited work or when explicitly requested.
```

## Common Tooling Patterns

Different assistants expose different controls, but the workflow is the same:

1. `ChatGPT`: use a project or workspace with the repo files attached
2. `Claude`: attach the repo files to the project context or custom instructions
3. `Gemini`: provide the repo files in the workspace and point the model to `AGENTS.md`
4. `Cursor`: keep the repository open and let workspace rules read from the repo root
5. `GitHub Copilot`: keep the repo open in the editor and point it at the root instruction files

## Quizme Mode

If the assistant understands `--quizme`, use it for exhaustive clarification before substantive work.
If it does not, use the assistant's closest equivalent to stop and clarify before it starts editing or running risky commands.
