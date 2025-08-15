Aegis Cognitive Mesh (ACM)
Aegis Cognitive Mesh (ACM) is an Azure‑native, highly secure, AI decision-making fabric that follows a “prove‑then‑execute” model for safe, auditable, and resilient decisions.

Core Capabilities
Confidential Compute to protect sensitive operations.

Azure Attestation to prove the environment is secure before taking action.

Secure Key Release (SKR) so secrets are only released after verification.

Azure Digital Twins to simulate real‑world systems (e.g., warehouses and delivery routes) before applying decisions.

Policy Verification using Z3 to ensure all actions follow defined rules.

Goals
Build a prove‑then‑execute system that:

Ensures decisions are safe and auditable.

Is resilient and suitable for production and interview scenarios.

Keeps costs controlled and operations deterministic.

Cost Hygiene
Use Azure for Students credits carefully; run compute only during tests/demos.

Set spend alerts; keep Digital Twins minimal.

Avoid expensive services (e.g., Managed HSM/Purview) in live environments unless necessary.

Prefer local development; keep simulations short and deterministic.

Architecture
See ops/architecture-v1.png (or architecture-template.txt) for the system layout.

Development
Git hooks
To enable the pre‑commit policy lock check locally:

Run:
bash scripts/setup_hooks.sh

This configures Git to use .githooks so the policy‑lock check runs on commit.

Verify policy lock locally
Show the current computed policy hash:
make policy-hash

Update the lock file to the current hash:
make policy-lock

The pre‑commit hook blocks commits if policies/base.yaml changes without updating policies/policy.lock.

Policy files and hashing
Source policy: policies/base.yaml

Lock file: policies/policy.lock

Deterministic hash generator: scripts/hash_policy.py

Only fields listed under hash_include in policies/base.yaml contribute to the canonical hash.

CI enforcement
A CI workflow verifies that the computed policy hash matches the value in policies/policy.lock. If they differ, CI fails and instructs contributors to update the lock file.

Common tasks
Compute current policy hash:
make policy-hash

Update policy lock after editing policies/base.yaml:
make policy-lock
git add policies/policy.lock
git commit -m "chore: update policy.lock after policy change"

If a commit is blocked by the pre‑commit hook with “Hash mismatch”:

Run make policy-lock

Re‑stage and commit.
