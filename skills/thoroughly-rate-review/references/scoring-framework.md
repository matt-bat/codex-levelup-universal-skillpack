# Scoring Framework

Use this reference only for an explicitly requested rating, score, grade, or benchmark.

## Default Categories

Adapt these to the domain rather than forcing irrelevant categories:
1. coverage and completeness: 14 percent
2. correctness and internal consistency: 18 percent
3. practical utility and user value: 14 percent
4. safety, risk control, and reliability: 14 percent
5. enforceability and operationalization: 14 percent
6. clarity and documentation quality: 10 percent
7. efficiency and maintainability: 6 percent
8. integration and cohesiveness: 10 percent

Weights must total 100 percent. For multi-component systems, retain an integration/cohesiveness category or explain the equivalent replacement.

## Check Structure

For each category:
1. define three to six observable checks
2. score every check on the same scale
3. compute category percentage from earned versus available points
4. multiply by category weight

Sum weighted contributions and round only at the end.

## Five-Point Anchors

1. `0`: absent or broken
2. `1`: major deficiencies
3. `2`: partial and unreliable
4. `3`: adequate baseline
5. `4`: strong and consistent
6. `5`: excellent and robust

## Confidence

Use `high`, `medium`, or `low` confidence based on source coverage and evidence quality. When evidence is missing, identify what would change the score instead of guessing.

## Modes

1. `quick`: fewer checks and a compact evidence summary
2. `standard`: full relevant categories and concise evidence
3. `deep`: expanded checks and scenario analysis when explicitly requested

## Comparison

1. Use identical weights and checks for every candidate.
2. Score candidates independently before ranking.
3. Show material tradeoffs, not only the winner.
4. Avoid false precision when candidates have uneven evidence.
