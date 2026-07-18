---
name: thoroughly-rate-review
description: Use only when the user explicitly asks to rate, score, grade, benchmark, or assign a numeric or weighted quality rating. Do not activate for a plain review, audit, assessment, evaluation, comparison, critique, or feedback request unless the user also requests scoring or a formal rubric.
---

# Thoroughly Rate Review

## Purpose
Produce an evidence-backed score when scoring is an explicit deliverable.

Plain review is excluded. If the user asks only for findings, feedback, risks, or recommendations, use the applicable review workflow without this skill and without inventing a score.

## Scoring Workflow
1. Define categories that match the object and user priorities.
2. Assign weights totaling exactly 100 percent.
3. Define observable checks and a stable scoring scale before judging.
4. Score each check from direct evidence.
5. Compute category contributions and the final score consistently.
6. Explain strengths, gaps, uncertainty, and the most valuable improvements.

## Evidence Rules
1. Cite the file, behavior, artifact, or observation behind each material score.
2. State assumptions and lower confidence when evidence is incomplete.
3. Do not use numerical precision greater than the evidence supports.
4. Apply the same framework to every item in a comparison.
5. Keep scoring separate from execution-risk or release-gate decisions.

## Artifact Boundary
Return the score in the response unless the user explicitly requests a durable report or an existing task already authorizes one. Activation alone does not authorize file changes.

## Conditional Reference
Read [Scoring Framework](./references/scoring-framework.md) only after explicit scoring intent is confirmed and a weighted model, comparison, or detailed scoring mode is needed.

## Output
1. framework and weights
2. category scores with concise evidence
3. final score and confidence
4. strongest qualities
5. highest-value improvements
