# Governance Walkthrough

[Documentation home](./README.md) · [Validation profiles](./validation-profiles.md) · [Release provenance](./release-provenance.md)

Use this flow for a new governed change or release. It records the exact scope, authority, catalog contract, evidence, and recommendation without granting any operation by itself.

## When to Use It

Create a schema-v3 governance pair when an authorized change touches a governed path:

1. `skills/**` or `.codex/skills/**`
2. `AGENTS.md` or `user-instructions.md`
3. `.github/workflows/**` or `.github/branch-protection-policy.json`
4. `docs/governance/**`
5. `docs/project-index.md`

The CI job runs for every pull request targeting `main`, but it requires a new plan only when the diff contains governed paths.

Do not create a durable artifact for read-only work. Do not reuse, modify, delete, or rebind a committed task artifact. Validate schema-v1 and schema-v2 files only as historical evidence; use a new task ID for new work.

## Choose Purpose and Authority

Use `--purpose change` for implementation, documentation, policy, or governance-tooling work. Bind only the normalized governed diff.

Use `--purpose release` only for an actual release decision with explicit `publish` authority. Release artifacts bind the full diff and require release metadata. A change artifact cannot substitute for a release artifact.

Record each authorized operation separately with repeated `--authorized-operation` options. For example, `configure_remote` does not authorize push, and push does not authorize remote configuration. Omit every operation that active instructions did not authorize.

Choose `scripted-command-execution` for a deterministic shell or API workflow. Choose `pseudo-agentic-automation` for adaptive browser or GUI interaction. Do not select both.

## Verify Remote Desired State

Treat `.github/branch-protection-policy.json` as the machine-readable desired state for the named GitHub repository and branch. Its `$schema` points to the closed `skills/skill-governance/schemas/remote-configuration-policy.schema.json` contract.

With repository read access and an authenticated GitHub CLI session, compare a fresh branch-protection response without mutating the remote by running the canonical command in [Protected-Main Snapshot](./release-provenance.md#protected-main-snapshot).

The verifier validates the desired-state schema, proves the API response URL names the policy repository and branch, normalizes only supported fields, and performs an exact comparison. Unknown API fields and any drift fail closed. Do not ignore newly introduced fields or silently accept partial conformance; update and validate the contract in a separately governed change when provider behavior evolves.

A successful verification is read-only, point-in-time evidence. It does not grant `configure_remote`, push, or any other mutation authority. A failure does not authorize automatic repair. Before an authorized remote change, preserve the actual before state and rollback procedure; after the change, rerun the same command and record its timestamped, content-anchored result.

## Finalize the Diff First

Resolve the exact base commit, complete the intended file changes, and run preliminary checks before generating the pair. The generator writes a pending `no-go` artifact and refreshes `docs/project-index.md`; its own JSON and Markdown paths are excluded from the bound manifest. Working-tree content is passed through Git's configured clean filters in an isolated temporary index, so the recorded hashes match the eventual commit even when local line endings differ.

The task ID must not exist at the enforced base. You may regenerate an uncommitted draft, but finish its evidence and binding before the pair's first commit.

## Generate a Change Artifact

Replace every placeholder and select only skills required by the catalog and current gates:

```sh
TASK_ID=YOUR_CURRENT_TASK_ID
BASE_SHA=FULL_BASE_COMMIT_SHA

python3 skills/skill-governance/scripts/generate_governance_artifact.py \
  --task-id "$TASK_ID" \
  --base-sha "$BASE_SHA" \
  --repo-root . \
  --skills-root skills \
  --project-id agent-command-center \
  --profile internal \
  --project-language Markdown/Python \
  --project-description-max4 "Agent command center" \
  --model-runs-test-build-default yes \
  --execution-scope local_only \
  --purpose change \
  --quizme-mode off \
  --behavior-or-workflow-changed \
  --skills-in-use "skill-governance,regression-prevention,scripted-command-execution,doc-maintenance" \
  --skills-execution-order "skill-governance,regression-prevention,scripted-command-execution,doc-maintenance" \
  --skills-selection-rationale "Governed behavior, regression evidence, deterministic validation, and documentation synchronization are required." \
  --execution-skill scripted-command-execution \
  --data-impact 0 \
  --business-impact 1 \
  --change-complexity 2 \
  --dependency-uncertainty 1 \
  --recoverability 1
```

Add operation authority only when explicitly granted. Use non-local scope for any authority other than commit:

```sh
  --execution-scope external \
  --authorized-operation commit \
  --authorized-operation push
```

Add `governance-enforcement` when governance tooling or release enforcement changes. Critical mode also requires `semantic-policy-audit` and `governance-enforcement`. Add `project-backup` and `--requires-backup` only for typed external loss exposure. Add `restore-drill` and `--requires-restore` when execution requires restore proof; authorized delete or migrate requires both controls.

While quizme mode is active, record its options and include `quizme-mode` plus its `requirement-clarifier` prerequisite. The schema-v3 startup declaration is always required as a durable catalog binding. Outside the artifact, show a user-facing startup declaration only when the user requested one or governed/audited work needs that durable routing record.

## Record Typed Gate Evidence

The generator initializes every required gate as pending and sets `recommendation` to `no-go`. After checks actually pass, replace each gate's status and evidence in the uncommitted JSON.

Use this evidence shape:

```json
{
  "status": "pass",
  "evidence": [
    {
      "kind": "test",
      "reference": "governance unit suite: all tests passed",
      "result": "pass",
      "observed_at_utc": "2026-07-18T00:00:00+00:00",
      "revision_sha": null,
      "sha256": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
    }
  ],
  "waiver_reason": ""
}
```

Use the real timestamp and the exact revision or digest of the referenced evidence. Choose a kind accepted by that gate; see [risk-and-gates.md](../skill-governance/references/risk-and-gates.md). Placeholder references, status-only passes, wrong kinds, missing timezones, or unanchored evidence fail validation.

Set `recommendation` to `go` only after every required gate passes. A permitted waiver requires enabled break-glass metadata and permits at most `go-with-risk`; `no-go` remains valid. Break glass never supports `go`, and `governance-enforcement`, `project-backup`, and `restore-drill` cannot be waived.

Regenerate the Markdown file from the final uncommitted JSON with the canonical renderer:

```sh
python3 - "$TASK_ID" <<'PY'
import json
import sys
from pathlib import Path

sys.path.insert(0, "skills/skill-governance/scripts")
from generate_governance_artifact import GovernanceArtifact, render_markdown

task_id = sys.argv[1]
json_path = Path("docs/governance") / f"{task_id}.governance.json"
md_path = Path("docs/governance") / f"{task_id}.governance.md"
artifact = GovernanceArtifact(**json.loads(json_path.read_text(encoding="utf-8")))
md_path.write_text(render_markdown(artifact) + "\n", encoding="utf-8")
PY
```

Do not hand-maintain a divergent schema-v3 Markdown summary.

## Validate Before the First Commit

Install the pinned structural validator dependency in the active environment, then run:

```sh
python3 -m pip install --disable-pip-version-check -r skills/skill-governance/requirements.txt
python3 skills/skill-governance/scripts/validate_skill_policy.py --agents-path AGENTS.md --skills-root skills --repo-root .
python3 skills/skill-governance/scripts/validate_skill_order_sync.py --skills-root skills
python3 skills/skill-governance/scripts/generate_routing_views.py --repo-root . --check
python3 -m unittest skills.skill-governance.tests.test_remote_configuration
python3 -m unittest discover -s skills/skill-governance/tests -p 'test_*.py'
python3 skills/skill-governance/scripts/validate_governance_artifact.py \
  --artifact "docs/governance/${TASK_ID}.governance.json" \
  --strict \
  --require-recommendation go
```

The governance validator fails closed when the pinned `jsonschema` dependency is unavailable. It applies Draft 2020-12 JSON Schema with format checking before semantic validation. `validate_skill_policy.py` also verifies exact JSON/Markdown equality.

`validate_skill_policy.py` validates the checked-in branch-protection policy against its closed schema. The focused remote-configuration test exercises target matching, unknown-field rejection, drift reporting, and standard-input verification through the script.

Record environmental blockers and residual risk. Never downgrade a failed or skipped check silently.

## Commit and Enforce the Exact Change

Commit the finished pair once, only when commit authority exists. Do not add a pending artifact in one commit and update it in another.

From the exact committed candidate, run normal enforcement:

```sh
BASE_SHA=FULL_BASE_COMMIT_SHA
CANDIDATE_SHA=FULL_CANDIDATE_COMMIT_SHA

test "$(git rev-parse HEAD)" = "$CANDIDATE_SHA"
test -z "$(git status --porcelain --untracked-files=all)"

python3 skills/skill-governance/scripts/enforce_governance_ci.py \
  --repo-root . \
  --skills-root skills \
  --base-sha "$BASE_SHA" \
  --head-sha "$CANDIDATE_SHA" \
  --strict \
  --require-recommendation go
```

Enforcement verifies the exact base and manifest, catalog digest/version/router contract at the candidate head, typed evidence, canonical pair, and append-only history across the base-to-head range.

The manifest binds repository content only. For remote-only work, keep exact target identity, before and desired settings, rollback steps, and post-operation readback in the typed evidence and audit trail; do not present the Git manifest as proof of external state.

## Generate a Release Artifact

First update the version, add a dated changelog heading, and create release notes. The release notes must contain:

1. The intended `v<version>` tag name.
2. `- Skill count: \`<exact catalog count>\``.
3. `- Governance test count: \`<exact test count>\``.

Generate a distinct release-purpose pair before the release commit:

```sh
TASK_ID=YOUR_RELEASE_TASK_ID
BASE_SHA=FULL_RELEASE_BASE_SHA
VERSION=X.Y.Z

python3 skills/skill-governance/scripts/generate_governance_artifact.py \
  --task-id "$TASK_ID" \
  --base-sha "$BASE_SHA" \
  --repo-root . \
  --skills-root skills \
  --project-id agent-command-center \
  --profile production \
  --project-language Markdown/Python \
  --project-description-max4 "Agent command center" \
  --model-runs-test-build-default yes \
  --execution-scope external \
  --purpose release \
  --authorized-operation publish \
  --release-version "$VERSION" \
  --release-tag "v${VERSION}" \
  --release-version-path skills/VERSION \
  --release-changelog-path skills/CHANGELOG.md \
  --release-notes-path "skills/RELEASE_NOTES_v${VERSION}.md" \
  --behavior-or-workflow-changed \
  --quizme-mode off \
  --skills-in-use "skill-governance,regression-prevention,semantic-policy-audit,governance-enforcement,scripted-command-execution,doc-maintenance" \
  --skills-execution-order "skill-governance,regression-prevention,semantic-policy-audit,governance-enforcement,scripted-command-execution,doc-maintenance" \
  --skills-selection-rationale "Release policy, regression evidence, semantic review, deterministic enforcement, and documentation synchronization are required." \
  --execution-skill scripted-command-execution \
  --business-impact 3 \
  --change-complexity 2 \
  --dependency-uncertainty 2 \
  --recoverability 3
```

Complete typed evidence and canonical pairing before the release artifact's first commit. The generator binds release purpose to the full diff and requires every release metadata path in that manifest.

## Verify the Exact Release Commit

Use a clean checkout at the exact candidate commit:

```sh
TASK_ID=YOUR_RELEASE_TASK_ID
CANDIDATE_SHA=FULL_CANDIDATE_COMMIT_SHA
ATTESTATION_PATH="/tmp/${TASK_ID}.attestation.json"

test "$(git rev-parse HEAD)" = "$CANDIDATE_SHA"
test -z "$(git status --porcelain --untracked-files=all)"

python3 skills/skill-governance/scripts/enforce_governance_ci.py \
  --repo-root . \
  --skills-root skills \
  --head-sha "$CANDIDATE_SHA" \
  --strict \
  --require-recommendation go \
  --release-check \
  --attestation-out "$ATTESTATION_PATH"
```

Release enforcement requires exactly one strict schema-v3 release artifact whose recorded base, full manifest, catalog binding, and metadata match the exact head.

If an authorized local tag already exists, verify it without changing it:

```sh
TAG_NAME=INTENDED_RELEASE_TAG
test "$(git rev-parse "${TAG_NAME}^{commit}")" = "$CANDIDATE_SHA"
```

Local verification does not prove a remote tag, branch protection, required checks, or publication state. Verify those separately when read authority exists. Creating a tag, pushing, publishing, or changing remote settings requires its own explicit authority.

## Ready Checklist

Before an authorized push or release action, confirm:

1. The exact candidate checkout is clean.
2. Policy, generated-view, governance, and regression checks pass at that commit.
3. The new pair is strict, canonical, append-only, and bound to the intended base and manifest.
4. Every operation is explicitly authorized and still unblocked at `pre_external_action`.
5. Relevant protected-branch state passes the closed desired-state verifier with no unknown fields or drift.
6. Release purpose, when applicable, has exact metadata, full-diff binding, one matching artifact, and an exact-head attestation.
7. Residual risk, skipped checks, and unverified external controls are stated explicitly.
