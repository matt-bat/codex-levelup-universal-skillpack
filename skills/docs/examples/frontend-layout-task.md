# Example: Frontend Layout Task

## Scenario
The user asks for UI layout, navigation, interaction, or visual-system work.

Frontend work should be judged by the experience, not only by whether the code compiles. The agent should think about the screen, responsive behavior, interaction states, and common user paths.

## Minimal Route
Select `ui-design-skills` when the authorized work needs general interaction, accessibility, or visual-quality judgment.

Add another skill only when its independent trigger appears:

1. `thoughtful-approach` when product behavior requires meaningful user-experience tradeoffs
2. `regression-prevention` for non-trivial implementation work
3. `effective-testing-methods` only when test design or test-file changes are in scope
4. `pseudo-agentic-automation` only for an authorized adaptive browser or GUI workflow

Never auto-select `ui-spatial-canvas` for generic frontend work. Use it only when the user explicitly requests Spatial Canvas or repository evidence establishes it as the existing interface architecture.

This routine route does not need a startup declaration unless the user explicitly asks for one or the work becomes governed or audited.

## Why
1. apply general design principles intentionally
2. add product, implementation, test, or execution owners only when their effects are in scope
3. protect responsive layout and interaction states
4. validate impacted UI paths proportionally

## Enough Validation
1. build or type check
2. targeted unit or component checks when present
3. Playwright or screenshot checks only when a browser-visible flow changed and runtime supports them
4. documented constrained-environment blocker when browser checks cannot run

## Stop Rule
Do not add decorative UI structure or marketing-style content unless the task calls for it.
