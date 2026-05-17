---
name: ui-design-skills
description: Use for building or reviewing UI design quality using principles synthesized from trusted UX sources (Apple HIG, Google Material, MIT HCI, Nielsen heuristics, WCAG).
---

# UI Design Skills

## Quick Index (Action-Routed)
### Read First (All Actions)
1. `Mission`
2. `Use This Skill When`
3. `Scope Boundary`
4. `Source Set (Trusted References)`
5. `Core Principles`

### Action Modules (Read As Needed)
1. Design framing:
   - `Step 1: Define User + Context`
   - `Step 2: Define Primary Tasks`
2. UI quality application:
   - `Step 3: Apply Principle Checklist`
   - `Step 4: Accessibility and Inclusion Gate`
   - `Step 5: Platform Adaptation Gate`
3. Verification:
   - `Step 6: Validation Evidence`
   - `Acceptance Checklist`

### Output
1. `Deliverable Format`
2. `Anti-Patterns`

## Mission
Provide a practical, source-grounded UI design standard that applies to any app domain and can be executed as deterministic design guidance.

## Use This Skill When
1. creating or revising UI layouts, flows, components, or visual systems
2. evaluating UI quality before implementation or release
3. resolving design tradeoffs with objective principles instead of preference-only debate
4. needing a common quality baseline across web/mobile/desktop apps

## Scope Boundary
This skill is UX/UI principle synthesis and application.

Use [UI Spatial Canvas](../ui-spatial-canvas/SKILL.md) when:
1. the requested interface should follow no-scrollbar viewport framing and root-level spatial navigation
2. interaction architecture is explicitly Spatial Canvas style

Use [Thoughtful Approach](../thoughtful-approach/SKILL.md) when:
1. product feature scope decisions (must-have versus nice-to-have) are the primary problem

## Source Set (Trusted References)
Primary references:
1. Apple Human Interface Guidelines:
   - https://developer.apple.com/design/human-interface-guidelines
2. Google Material Design:
   - https://m1.material.io/
3. MIT 6.813/6.831 User Interface Design and Implementation:
   - https://web.mit.edu/6.813/
   - https://web.mit.edu/6.813/www/sp16/classes/01-usability/
4. Nielsen Norman Group usability heuristics:
   - https://www.nngroup.com/articles/ten-usability-heuristics/
5. W3C WCAG 2 Overview:
   - https://www.w3.org/WAI/standards-guidelines/wcag/

Reference policy:
1. these sources define baseline principles
2. when sources conflict, prioritize accessibility and platform conventions for the target platform
3. if platform-specific UX rules are strict (for example iOS or Android), adapt patterns to match native expectations

## Core Principles
### 1) Clarity and Hierarchy
1. primary actions and information must be visually obvious
2. use size, spacing, contrast, and position to establish scan order
3. every screen should have one clear primary intent

### 2) Consistency and Predictability
1. similar controls must behave the same way
2. naming, icons, spacing, and interaction patterns should stay stable across flows
3. follow established platform conventions unless a documented usability reason requires deviation

### 3) Visibility of System Status
1. always show state changes and progress in reasonable time
2. loading, success, empty, and error states must be explicit
3. long-running actions need progress or staged feedback

### 4) Match Real-World Mental Models
1. use user language instead of internal engineering terminology
2. organize flows in natural task order
3. use familiar metaphors only when they improve understanding

### 5) User Control and Recovery
1. support cancel/undo for non-trivial actions where feasible
2. avoid irreversible destructive actions without confirmation or clear safeguards
3. make exits and back paths obvious

### 6) Error Prevention and Resilience
1. prevent invalid input early with inline guidance
2. validate at the right moment to minimize surprise failures
3. error messages must explain what happened and how to recover

### 7) Recognition Over Recall
1. prefer visible choices over hidden commands
2. keep important controls discoverable
3. reduce memory load with defaults, previews, and contextual hints

### 8) Efficiency and Progressive Disclosure
1. optimize core paths for low step-count
2. keep novice flows obvious while enabling expert shortcuts
3. reveal advanced options progressively to reduce clutter

### 9) Accessibility and Inclusion by Default
1. design for keyboard, touch, and assistive technology use
2. ensure sufficient color contrast and visible focus states
3. ensure text alternatives, semantic labeling, and robust form messaging
4. target WCAG 2.2 AA unless explicit constraints are documented

### 10) Responsive and Adaptive Layout
1. layouts must adapt to mobile/tablet/desktop breakpoints
2. preserve task completion capability across screen sizes
3. adapt to platform conventions where divergence improves comprehension

### 11) Motion and Visual Restraint
1. motion should communicate transitions and causality, not decoration
2. visual effects should not reduce readability or increase cognitive load
3. respect reduced-motion and accessibility preferences

### 12) Content-First Interface Discipline
1. UI chrome should support task completion, not dominate it
2. remove non-essential elements that do not help decisions or actions
3. maintain deliberate whitespace and grouping for comprehension

## Step 1: Define User + Context
For each surface, identify:
1. primary role(s)
2. primary intent
3. critical constraints (platform, accessibility, legal, locale)

## Step 2: Define Primary Tasks
1. list top 3 to 5 tasks users must complete
2. mark one primary action per task surface
3. identify where users most likely fail or hesitate

## Step 3: Apply Principle Checklist
For each task flow:
1. check every core principle (1 through 12)
2. mark each as `pass`, `partial`, or `fail`
3. for `partial`/`fail`, propose a minimal corrective design change

## Step 4: Accessibility and Inclusion Gate
Required checks:
1. keyboard path for all critical actions
2. visible focus indicators and logical focus order
3. contrast and text scaling resilience
4. non-color cues for important state differences

## Step 5: Platform Adaptation Gate
1. confirm adherence to target platform conventions
2. document any intentional deviations and rationale
3. verify that custom patterns remain learnable for first-time users

## Step 6: Validation Evidence
Minimum evidence:
1. before/after flow snapshot or concise change list
2. principle checklist results by flow
3. accessibility gate pass/fail summary
4. unresolved risks and mitigation path

## Acceptance Checklist
1. primary tasks are discoverable within first screen context
2. each surface has one clear primary action
3. core states (loading/empty/error/success) are defined
4. accessibility gate passes or has documented exceptions
5. platform adaptation decisions are documented
6. no high-severity `fail` remains without mitigation

## Deliverable Format
When applying this skill, provide:
1. user/context assumptions
2. task-flow map and primary actions
3. principle checklist summary (`pass`/`partial`/`fail`)
4. accessibility + platform gate results
5. design changes made or recommended
6. open risks and next remediation step

## Anti-Patterns
1. aesthetic-driven redesign with no task outcome improvement
2. inconsistent components across similar flows
3. hidden primary actions requiring memory or guesswork
4. inaccessible interactions treated as optional fixes
5. using one platform's pattern in another without adaptation rationale

## Related Skills
- [UI Spatial Canvas](../ui-spatial-canvas/SKILL.md): apply Spatial Canvas interaction architecture when explicitly requested.
- [Thoughtful Approach](../thoughtful-approach/SKILL.md): prioritize user-value scope decisions.
- [Regression Prevention](../regression-prevention/SKILL.md): protect behavior while implementing UI changes.
- [Doc Maintenance](../doc-maintenance/SKILL.md): keep UX documentation synchronized with implementation.
- [Token Reduction](../token-reduction/SKILL.md): keep design rationale concise and high-signal.
