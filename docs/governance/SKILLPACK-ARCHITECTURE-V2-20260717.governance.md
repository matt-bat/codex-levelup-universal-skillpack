# Governance Artifact: SKILLPACK-ARCHITECTURE-V2-20260717

- `schema_version`: 2
- `created_at_utc`: 2026-07-18T01:09:32.410442+00:00
- `project_id`: agent-command-center
- `profile`: internal
- `project_language`: Markdown/Python
- `project_description_max4`: Agent command center
- `model_runs_test_build_default`: yes
- `execution_scope`: local_only
- `deployment_requested`: false
- `execution_skill`: scripted-command-execution
- `quizme_mode`: off
- `quizme_multiple_choice`: false
- `quizme_one_at_a_time`: false
- `quizme_confirm`: false
- `quizme_record`: false
- `selected_mode`: critical
- `total_score`: 10
- `recommendation`: go

## Scores
- `data_impact`: 1
- `business_impact`: 2
- `change_complexity`: 3
- `dependency_uncertainty`: 3
- `recoverability`: 1

## Critical Overrides
- none

## Required Gates
- [x] `scripted-command-execution` (status: pass)
  - evidence: deterministic local command plan completed; no external mutation or release action executed
  - waiver_reason:
- [x] `regression-prevention` (status: pass)
  - evidence: 101 unit tests and 25 typed routing scenarios passed
  - waiver_reason:
- [x] `semantic-policy-audit` (status: pass)
  - evidence: catalog mutation tests, adversarial boundary fixtures, and semantic drift scans passed
  - waiver_reason:
- [x] `governance-enforcement` (status: pass)
  - evidence: policy, ordering, catalog, schema, YAML, compilation, workflow-parity, history-integrity, manifest-binding, and strict artifact checks passed
  - waiver_reason:
- [x] `doc-maintenance` (status: pass)
  - evidence: public and internal documentation synchronized; 207 relative links passed
  - waiver_reason:

## Startup Declaration
### Skills In Use
- `skill-creator`
- `internal-lang`
- `hyperfocus-discovery`
- `token-reduction`
- `skill-governance`
- `project-backup`
- `restore-drill`
- `semantic-policy-audit`
- `interdependent-change-planning`
- `order-of-operations`
- `scripted-command-execution`
- `regression-prevention`
- `governance-enforcement`
- `deprecation-management`
- `doc-maintenance`
- `user-instructions-tracker`
### Skill Selection Rationale
Skill creation guidance governed the skill rewrites; typed governance, ordering, regression, semantic audit, deprecation, documentation, and instruction tracking controlled the cross-cutting migration; backup and restore evidence preserved the pre-change state used at task startup.
### Skill Execution Order
- `internal-lang`
- `hyperfocus-discovery`
- `token-reduction`
- `skill-creator`
- `skill-governance`
- `project-backup`
- `restore-drill`
- `semantic-policy-audit`
- `interdependent-change-planning`
- `order-of-operations`
- `scripted-command-execution`
- `regression-prevention`
- `governance-enforcement`
- `deprecation-management`
- `doc-maintenance`
- `user-instructions-tracker`

## Evidence Requirements
- [x] mode + score: critical mode, total score 10
- [x] impact map: catalog, router, safety gates, governance evidence, skills, documentation, compatibility, and CI policy
- [x] validation scope by layer: skill format, unit, fixture, schema, policy, generated views, workflow, link, history, and bound-artifact checks
- [x] residual risks: routing normalization still depends on caller-supplied typed intent; observation evidence is intentionally immature
- [x] rollback plan: verified pre-change backup at `/tmp/agent-command-center-backup.73uurC/workspace` and restore drill at `/tmp/agent-command-center-restore.RJskX4/restored`
- [x] release decision: local implementation is go; public release remains no-go until an authorized commit, exact-head attestation, release validation, and remote protection review

## Break Glass
- enabled: false

## Notes
Local-only version 2 architecture migration; no push, publish, release, deployment, or remote settings change authorized.

## Change Binding
- `base_sha`: 9ef4b74604af601322d3616b85d408be8fec4c5f
- `manifest_sha256`: 347dad9f97b0cd688e51667f0fcb8c525a1fed3a84574b2ce811d9585421d7a4
- `manifest`:
  - `M` `.github/workflows/skills-governance-ci.yml` (`sha256`: ebd55848fcee4363e1bbba35e558791f747ce0ef1e54ea6aa0796674b688a74a)
  - `M` `AGENTS.md` (`sha256`: fc494e742e5794daeb64e6f1aa50fae7b8fce6ff51e495e1c64bbe83169de31a)
  - `M` `docs/project-index.md` (`sha256`: 7bd4122c59dfea35cf77dcdecebacccbc16e10921788fd5c910e85f42ec56842)
  - `M` `skills/.gitignore` (`sha256`: 73cef5fec3e121bc61d3561a03b73cc2cab091efede309c122a5f809299c5545)
  - `M` `skills/CHANGELOG.md` (`sha256`: 6a9ed1929042019d1a76b59a001a2905b72c3a24365eb9f854b9ca9f06a42b6c)
  - `M` `skills/README.md` (`sha256`: d0717b57e25922900db0e9022f103bae3f58bf05fa794b574e1468f8f0d18282)
  - `M` `skills/SKILL-MAP.md` (`sha256`: b4be8c71de4cad0d45eb5f9c885ebc6e51008ed2918f7b02d09cf4081573d4fa)
  - `M` `skills/USAGE.md` (`sha256`: 8c2f9ac3301e82fcf01843652c53d11c289ae8ebfd1e739e6d8e39e171406fcd)
  - `M` `skills/deprecation-management/SKILL.md` (`sha256`: 3a1e3712abb530c8c9f6a4d6fa920e033cc722160e038d5efcc09d7d5b32746b)
  - `M` `skills/doc-maintenance/SKILL.md` (`sha256`: 12da1777fb3c6bd8f3daefccd86882181ad6c49babcc737e0857e7f11fece314)
  - `A` `skills/doc-maintenance/references/documentation-validation.md` (`sha256`: 6de7e4e372540d4fb41b1425ff407afc33d508afd41174420b89c411a43d5232)
  - `M` `skills/docs/adapters/agent.md` (`sha256`: f5de0fa2ab72f6176f136f61c46c4b6c812b0b418c6f6ef80dd390f2a0276026)
  - `M` `skills/docs/adapters/common-ai.md` (`sha256`: 6478c6308ff30c3e5cb5a20900640bc0300ad985057255d79364fa45e5956811)
  - `M` `skills/docs/adapters/generic-agent.md` (`sha256`: f9cdb2fc41403545c01f18904401bb3e43519302c84c337a326adffe28c61e8a)
  - `M` `skills/docs/cache-budgets.md` (`sha256`: 5e63c1cbb26336028805cf04b1e6ee3e7a33a137e1b712b46e89c917175ab450)
  - `M` `skills/docs/ci/skills-governance-ci.yml` (`sha256`: ebd55848fcee4363e1bbba35e558791f747ce0ef1e54ea6aa0796674b688a74a)
  - `M` `skills/docs/conflict-resolution-matrix.md` (`sha256`: 04ae1bbb3da30500bfaebf39a2d88c311c3f7be67aa3aa84a5a779b00466c572)
  - `M` `skills/docs/examples/bug-investigation.md` (`sha256`: 19bbf52908f93f0fe790ccbed5d84e3e51de4310c0263b4aac8474aee7bb0648)
  - `M` `skills/docs/examples/documentation-only-update.md` (`sha256`: 1798c75433523d022a0fae87cab0ba80fa6ed5279b5c53ed687df46eb295b58c)
  - `M` `skills/docs/examples/frontend-layout-task.md` (`sha256`: 1d9cb8d9bb58de95d8ec2ef693a78427f5a1579bb0d3a70e5c8664f0e2b158f8)
  - `M` `skills/docs/examples/quizme-clarification.md` (`sha256`: f8b3779e31d0483353c11b9efd2a12ef3df125e5b9e9bf25f12c98fc6f835bdb)
  - `M` `skills/docs/examples/release-readiness-change.md` (`sha256`: 2e0aa10cf86f856fa537494a9b89616ba4ff29e8e39631317ef779ea144c73d2)
  - `M` `skills/docs/examples/simple-code-fix.md` (`sha256`: 063c0c6249e49ab4dfef2271bdd6b1ec62e6c12eb1aa8213230cabbcae89ff02)
  - `M` `skills/docs/field-notes.md` (`sha256`: 5aae1a20c8ceb6d726cb969d585fb1d3db8a4090ea5f42bda93b0bc9e021ed0f)
  - `M` `skills/docs/governance-walkthrough.md` (`sha256`: 45ba10831b0cf38220dbf2988bb268a001dbce5c8edbb5d8d31bd84cae5c5e95)
  - `M` `skills/docs/install-profiles.md` (`sha256`: 5f7445bf4b2049d2284a37149b802dfda344da93f0b11268d2e9ea1eef3caeaf)
  - `M` `skills/docs/known-limitations.md` (`sha256`: f03aaea3d82f9c48125ad6de4fb16245df9ec2bb570ffeb9169e3b3930774a3c)
  - `M` `skills/docs/maturity-model.md` (`sha256`: 3db23c3a2d54d0f3acee21b528502ff3c5cea920bd536c005245a34eae0b2679)
  - `M` `skills/docs/pruning-policy.md` (`sha256`: 769a5db559cf676890e03c9e68b691541def8b6aa884b92254cf3ff7df505b1c)
  - `A` `skills/docs/release-provenance.md` (`sha256`: 6d76e5aa966493cc444e4f297ae3d42bb1acf44112d3a673e1e37fa7be9bceef)
  - `A` `skills/docs/routing-architecture-v2.md` (`sha256`: 1f7ecb101590e0b4d5398c4f3ffa0bd135d145ddf5665414b94f0385f451138b)
  - `M` `skills/docs/rubrics/release-readiness-rubric.md` (`sha256`: 4a32333807c1e3c74b45fb288d3286d8b89993bd44d7c56724be10e742763667)
  - `M` `skills/docs/skill-decision-tree.md` (`sha256`: 383121ccea23f54323dd6b0c142fcb688ce173bbefd76cd2ac7fe12dbdde3f75)
  - `M` `skills/docs/skill-index.md` (`sha256`: 65b3b27298d86e3533e403567aa649d3209b3ecb65c71345a121846acf70e478)
  - `A` `skills/docs/skill-migration-v2.md` (`sha256`: 7795874530123cae5fd63d91ecb6a7ca9bf7bd3c2e5ede77d3704a410c98afac)
  - `M` `skills/docs/validation-profiles.md` (`sha256`: 01b3225eccf57a7164d4cd706fab66e1403c81ffa9c8a50c7d37835d9c6b2340)
  - `M` `skills/docs/validator-severity-levels.md` (`sha256`: 33f865ff1681212e42c7d35fc98b9ea2f8e8512747254b749fce991c9d3caa59)
  - `M` `skills/effective-testing-methods/SKILL.md` (`sha256`: 7ba7c0a457d5a53a65fb818b07211fe3ae20ee96e851483f96eec77ecdea6697)
  - `A` `skills/effective-testing-methods/references/test-patterns.md` (`sha256`: 38fdc8a49dc6eb67923038e2c778d5f6fdfb956677c1f0b42f8fb15f15018ba2)
  - `M` `skills/governance-enforcement/SKILL.md` (`sha256`: 93fbfb9821b6afd28cb2a2fdc7d55dfe932b105bc864a80cdacccf0f419a32d9)
  - `M` `skills/history-indexing/SKILL.md` (`sha256`: a63c7bc9ccd44a1a1d25507a297092e373792f8fd54d4d61cd4e86fa0b85fb0b)
  - `A` `skills/hyperfocus-discovery/SKILL.md` (`sha256`: 42ae0646116305cb012c96e1935622a9d4ba14365ee8d903afabc5e2537bb920)
  - `A` `skills/hyperfocus-discovery/agents/openai.yaml` (`sha256`: 31d27de489ae0bdf3f8c5db6ccf2a1c4d41cf69e710a36176f3fc1c8da4cb2b5)
  - `A` `skills/hyperfocus-discovery/references/branch-management.md` (`sha256`: 3c1f30d6682396b29d97fa2368bada3cfebdb10352dde236e216393d6396d869)
  - `M` `skills/interdependent-change-planning/SKILL.md` (`sha256`: fbc6511c4616f3715fb0bad2167caafd69873bc5e0d4ef84ba467a2bd75e0f26)
  - `A` `skills/internal-lang/SKILL.md` (`sha256`: 961dc7910387accb2dd31f8759145bf2b5f6c1e277f6c3221ce65a96ea29a237)
  - `A` `skills/internal-lang/agents/openai.yaml` (`sha256`: c794c14f1ab49388aadfb4e4109a79085583aff65c3747ece3c3e19f6c8c18e2)
  - `A` `skills/internal-lang/references/notation-and-safety.md` (`sha256`: c05c7ea92655dd255ebb745c6202342d192802cc9f223c43012c53d43a64804e)
  - `M` `skills/order-of-operations/SKILL.md` (`sha256`: fc59ee9bb333d489167353d3c87478fce5eefc834420a8af5efc09a423bc12a7)
  - `A` `skills/order-of-operations/references/sequencing-playbook.md` (`sha256`: d788fdd8596d6cd315404d291600c0818343fda54cb1f7983d24bd557291a5d1)
  - `M` `skills/process-budget-controller/SKILL.md` (`sha256`: 410c2a550855acadb78158373721ed424a63692cea801458d96c8203a0097ecd)
  - `A` `skills/process-budget-controller/references/migration.md` (`sha256`: 54fd3c27dff98688db9c3211cfb46c1c5c70394ef36e17538628aa00b623e1d5)
  - `M` `skills/project-backup/SKILL.md` (`sha256`: bd41a1d4eacb65fd4ed2bd195726bb5a3bfa12c8a7a7cef4fc9304b902e6de92)
  - `A` `skills/project-backup/references/backup-runbook.md` (`sha256`: afde5394f1a4adee9d8696e58a26aff2f182a88956e0fb4a4a3a8b8278ec5b1b)
  - `M` `skills/pseudo-agentic-automation/SKILL.md` (`sha256`: 8b640ed0e9f90d3de9e22e591d9711677ce3a5796383ecd9ba37a211be18bf89)
  - `M` `skills/regression-prevention/SKILL.md` (`sha256`: fd6b43cd57d841adcbb86b872678b032183466aa41c6211e79b2ab64a89be3b1)
  - `A` `skills/regression-prevention/references/code-review.md` (`sha256`: 637e62ff6e58ba113beb4aead80020aa8bda7eac9ab5c34f0e6f3ffd0c9ca220)
  - `A` `skills/regression-prevention/references/compatibility-and-migrations.md` (`sha256`: 41952c9632933d4d8a403d15fd21a34fbe7aaa36f6d0c4cbaf11f8be203e836f)
  - `A` `skills/regression-prevention/references/implementation-quality.md` (`sha256`: 0866935624226b131de8e2b7e35fc4a96f6d79354599a35b5dc810ad5957ce06)
  - `M` `skills/requirement-clarifier/SKILL.md` (`sha256`: 9387c49e50b5665ff67742cc7f9cefb3189a5d57c259923c3be28d4d68f2f9e9)
  - `A` `skills/requirement-clarifier/references/task-contract-schema.md` (`sha256`: 3f411f798fda8372c1f2c27ae9b3805bc3ced898ead421be3d12ceddf6ab623b)
  - `M` `skills/restore-drill/SKILL.md` (`sha256`: bf13025215860bceeaa389ae69e08bd9eaf18e1a589a74c939ff657032ea896c)
  - `A` `skills/restore-drill/references/restore-drill-runbook.md` (`sha256`: 1cd0b5c9850fdf59c0dbd2c09ebc04158547a47c57e2e31f2238ebf57658ab81)
  - `M` `skills/scripted-command-execution/SKILL.md` (`sha256`: 3ae9481fee19e38f2c6dd46dab6965889c3bf7723c117f54cb7ecf6a4248f338)
  - `M` `skills/semantic-policy-audit/SKILL.md` (`sha256`: 9da2d34c863ff018962b30b4ca1217016d7a982d0e034747dfb227e92b2a919b)
  - `M` `skills/skill-catalog.json` (`sha256`: c3a4113b53d644384f770773dc31f664c6db152d5f17cbe504b343c657cb9e90)
  - `A` `skills/skill-catalog.schema.json` (`sha256`: 0a8655b2282e143fe63983c4f817e1af51293e3a5f70491028c8ea9f0903da0f)
  - `M` `skills/skill-governance/SKILL.md` (`sha256`: b53d62b0f1c790b88295166440c1d0b889fcc5a2b61e0634122aaaf24346cbc5)
  - `A` `skills/skill-governance/fixtures/routing-scenarios.json` (`sha256`: bda3dd34f48fb17f604e95c4fcf7c05ef8111c7d2e1f4d6697d4215a4cee49be)
  - `A` `skills/skill-governance/references/governance-artifacts.md` (`sha256`: 23ca775142d3ceb7439dbc71bec8a8581272ccafda7d208e41b526359b4f6161)
  - `A` `skills/skill-governance/references/risk-and-gates.md` (`sha256`: 603bca4172fd988673bcc0ee2f8096a1499b5bea296a8d7a240b851d541f725c)
  - `A` `skills/skill-governance/schemas/governance-artifact.schema.json` (`sha256`: f5af6b38237c8771efb948f3c73d4f1d67db62241efb92e66c73043b0a5c9831)
  - `A` `skills/skill-governance/schemas/routing-result.schema.json` (`sha256`: 2d8fec9729f881894f6b679b56e3037eb015e882d854904ddb0774411f462474)
  - `A` `skills/skill-governance/schemas/task-descriptor.schema.json` (`sha256`: fe12887f9cbb7ac3eed9569bad1b00ffc153a5371feb685975028e8db450f475)
  - `M` `skills/skill-governance/scripts/enforce_governance_ci.py` (`sha256`: a5c8f74c8e3d5547cb75d3d32b757f8536ae71fbb7082fb628e0d890e01bc012)
  - `M` `skills/skill-governance/scripts/generate_governance_artifact.py` (`sha256`: 9a9a1e895f9e0b1132030b6dcb3087f8c50924d28cbafa68cce6073f21d35819)
  - `A` `skills/skill-governance/scripts/generate_routing_views.py` (`sha256`: 1df83fd0d635ac03eeaca3ff60dab4048cabeb52124825de67092327468f8b5b)
  - `A` `skills/skill-governance/scripts/governance_common.py` (`sha256`: ba884ed89912b86c3e46fccfa88720a2bd5da98a3a8c8b9508d53a4926e28db4)
  - `A` `skills/skill-governance/scripts/record_routing_observation.py` (`sha256`: 711f9581279915b47077f0ec877505cab1e63fef408570faed49fa434dc4435a)
  - `A` `skills/skill-governance/scripts/resolve_task_route.py` (`sha256`: 71c0ab6ae9c06c5172a1b679d17df4bf862658eee5cea9f07b82a6e33ef15a4a)
  - `M` `skills/skill-governance/scripts/validate_governance_artifact.py` (`sha256`: ef9c89fa7f99248a8d3f102d9c4386d5719ad2df3f0bd819b12859903360277c)
  - `M` `skills/skill-governance/scripts/validate_skill_order_sync.py` (`sha256`: 5bebb3be8f72a877aa20615480a3c132b3673e03437e2ca980131c7807986ae3)
  - `M` `skills/skill-governance/scripts/validate_skill_policy.py` (`sha256`: a2bd91f5c28155704a9e5ccb1e8760a5b9e22e7f4c074101fd6a551ed98d727d)
  - `A` `skills/skill-governance/tests/test_default_skill_quality_gates.py` (`sha256`: ece97c611dbb82f190274c51c05f1f583bcbb64d6925c4a8842fd4499ebd27a2)
  - `M` `skills/skill-governance/tests/test_generate_governance_startup.py` (`sha256`: 28ded566739164f859ffb12d40b397f72cdcc4da6a45046789f083dc9ee00a56)
  - `A` `skills/skill-governance/tests/test_generate_routing_views.py` (`sha256`: 51b136b01d1380045c0ab1e9c67a6b95bb930e4f06a782b94609e601e826d514)
  - `A` `skills/skill-governance/tests/test_governance_integrity.py` (`sha256`: 0d1539364b6574d31d70a5f573ca9f445423ac020040932e92543327429fac99)
  - `A` `skills/skill-governance/tests/test_routing_observation.py` (`sha256`: b85a74590827569688fae2db2fb1623c6d81244ce4d070ff50f944dc5e4a8ad2)
  - `A` `skills/skill-governance/tests/test_task_routing.py` (`sha256`: 288a60e6f1eecf243b6df958885591b695ae9c40e282787a21cae56e48c75a5b)
  - `M` `skills/skill-usage-review/SKILL.md` (`sha256`: 300b4e63002e6840148a6eb35e093c424c96c85c094734beae688e33908adb77)
  - `M` `skills/thoroughly-rate-review/SKILL.md` (`sha256`: b0ca43f9be575c903bb6cf5fc421af9fbf8cb2debe4fec64d146d169339fb468)
  - `A` `skills/thoroughly-rate-review/references/scoring-framework.md` (`sha256`: 6569084bee11e27819d3bab1a24f4ce3eda349952bf5ee9b592673978e205e88)
  - `M` `skills/thoughtful-approach/SKILL.md` (`sha256`: deab1aa3fbff58107ffe233e10d3bc09a643241a5023aa6048853bcb1014a3f7)
  - `M` `skills/token-reduction/SKILL.md` (`sha256`: 27913e6c73fdb1b2d02e72df67b0b69fe338fc7198792702394a2b35da4a0258)
  - `A` `skills/token-reduction/references/context-and-output-controls.md` (`sha256`: fd3ca735bae839c3ae567fa219fd8e8b500a150e2793f0783677f9b1c97d7f44)
  - `A` `skills/token-reduction/references/legacy-project-intake-compatibility.md` (`sha256`: f97f121431254d461431b908366f29f50c220618f3c71289a49146307296715b)
  - `M` `skills/ui-spatial-canvas/SKILL.md` (`sha256`: 85e222d42343f479058aaea9fe362f56d93ea3910d16cb5da0f862f3feb7cdf3)
  - `A` `skills/ui-spatial-canvas/references/spatial-canvas-system.md` (`sha256`: e6c72e53226b13c64776d6627a8a336a7bb6abe4d68c29365146cb4a623a709b)
  - `M` `skills/user-instructions-tracker/SKILL.md` (`sha256`: 3977308dfbfe3dba59f523b35eaa3477a123101d0a04167d2e68bc859dd4e4e5)
  - `A` `skills/user-instructions-tracker/references/tracker-schema-and-lifecycle.md` (`sha256`: dd9540c8a9d57b8b5b56e62bad5ed3db5f2d9cbaf23bd36b18cc497b6265019b)
  - `M` `skills/user-instructions.md` (`sha256`: 19d270757334b167ae84fbbfbfcb9265e7ae518c153a75b856d76df5bd609fe4)
