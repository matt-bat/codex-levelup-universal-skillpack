# Evidence And Pivot Patterns

Use this reference when a challenged approach needs a disciplined reset or a structurally different alternative. These sources inform the workflow; they do not imply that human psychological traits map directly onto language models.

## Evidence-To-Rule Map

| Evidence | Relevant finding | Operational rule |
|---|---|---|
| [Staw, “Knee-Deep in the Big Muddy” (1976)](https://doi.org/10.1016/0030-5073%2876%2990005-2) | Negative consequences can increase commitment to a chosen course under some conditions. | Ignore past investment when deciding whether the next attempt is justified. |
| [Leary et al., “Cognitive and Interpersonal Features of Intellectual Humility” (2017)](https://doi.org/10.1177/0146167217697695) | Intellectual humility centers on recognizing that one's beliefs may be wrong and is associated with openness and curiosity. | Make belief revision and calibrated confidence explicit; avoid performative self-deprecation. |
| [Cannon and Edmondson, “Failing to Learn and Learning to Fail Intelligently” (2005)](https://doi.org/10.1016/j.lrp.2005.04.005) | Learning from failure depends on identifying, analyzing, and deliberately experimenting rather than merely celebrating failure. | Convert failure into a tested update and a bounded experiment. |
| [Huang et al., “Large Language Models Cannot Self-Correct Reasoning Yet” (ICLR 2024)](https://openreview.net/forum?id=IkmD3fKBPQ) | Intrinsic correction without reliable external feedback can underperform the original response. | Do not run free-form “rethink” loops; require evidence or a discriminating verifier. |
| [Kamoi et al., “When Can LLMs Actually Correct Their Own Mistakes?” (TACL 2024)](https://aclanthology.org/2024.tacl-1.78/) | Self-correction is most dependable when tasks provide reliable external feedback. | Prefer tests, tools, specifications, and direct observations over self-generated critique alone. |
| [Gick and Holyoak, “Analogical Problem Solving” (1980)](https://doi.org/10.1016/0010-0285%2880%2990013-4) | Structurally useful solutions can transfer from semantically distant domains, but transfer often needs an explicit cue. | Search deliberately for structural analogies, then verify constraint correspondence. |
| [Stanovich and Toplak, “Actively Open-Minded Thinking and Its Measurement” (2023)](https://doi.org/10.3390/jintelligence11020027) | Active open-mindedness includes seeking alternatives, attending to contradictory evidence, and postponing premature closure. | Generate competing hypotheses and test evidence that could disconfirm the favored one. |
| [Barkett, Long, and Kröger, “Getting out of the Big-Muddy” (2025 preprint)](https://arxiv.org/abs/2508.01545) | Escalation behavior in tested LLM settings was context-dependent and especially pronounced in some social or compound-pressure conditions. | Treat escalation as situational, not inevitable; keep peer consensus or prior endorsement from substituting for evidence. |

## Pivot Triggers

Use a pivot checkpoint when one or more conditions hold:

1. the expected observation and actual observation diverge materially
2. a retry reproduces the same failure without testing a new cause
3. new authoritative evidence invalidates a premise
4. a user correction changes the task model
5. a workaround grows while the original acceptance criterion remains unmet
6. the explanation for continuing refers mainly to effort already spent

## Candidate Lenses

Generate alternatives by changing one governing dimension at a time:

1. **Mechanism:** replace the algorithm, tool, API, or execution engine.
2. **Representation:** change data shape, intermediate form, abstraction level, or visual model.
3. **Boundary:** move validation, transformation, or ownership to a more reliable layer.
4. **Direction:** work backward from the observable success state or invert a dependency.
5. **Baseline:** remove optional machinery and prove the smallest end-to-end path.
6. **Analogy:** map the constraint structure to a distant solved problem, then test every mapped constraint.

Do not generate many cosmetic variants. Two independent mechanisms are more useful than ten restatements.

## Discriminating Probe Template

```text
Competing candidates: A / B
Different governing assumption: ...
Probe: ...
If A is viable, observe: ...
If B is viable, observe: ...
Result: ...
Decision: continue A / continue B / gather missing evidence / ask user
```

## Failure-Learning Template

```text
Goal: ...
Observed evidence: ...
Invalidated premise: ...
Reusable result: ...
Abandoned method: ...
Next discriminating probe: ...
```

Keep this conversation-local unless a durable artifact is explicitly authorized and useful to a named consumer.
