# Code Review Checklist

Review in this order:

1. correctness and requirement coverage
2. data loss, authorization, and security boundaries
3. compatibility and migration behavior
4. failure handling, retries, and partial state
5. concurrency and performance where applicable
6. test relevance and missing negative cases
7. maintainability only when it creates concrete future risk

Use severities:

- `critical`: likely catastrophic loss, compromise, or unusable release
- `high`: likely user-visible failure, security defect, or incompatible behavior
- `medium`: real defect with bounded impact or an important unhandled case
- `low`: concrete maintainability or reliability issue with limited impact

For each finding, provide location, failure mechanism, impact, and the smallest credible remediation. Do not inflate preferences into defects.
