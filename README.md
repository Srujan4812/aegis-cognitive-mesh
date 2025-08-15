# Aegis Cognitive Mesh (ACM)

This project is an Azure‑native, highly secure, AI decision-making fabric.
It uses:
- **Confidential Compute** to protect sensitive operations.
- **Azure Attestation** to prove our environment is secure before taking action.
- **Secure Key Release (SKR)** so secrets are only given out after verification.
- **Azure Digital Twins** to simulate real-world systems (like warehouses and delivery routes) before applying decisions.
- **Policy Verification** using Z3 to ensure all actions follow defined rules.

Goal: Build a “prove‑then‑execute” system that can make safe, auditable, and resilient decisions — perfect for a production and interview scenario.


- **Cost Hygiene**

Use Azure for Students credits carefully; run compute only during tests/demos.

Set spend alerts; keep Digital Twins tiny; avoid Managed HSM/Purview live.

Prefer local dev; short, deterministic simulations.

-**“Architecture”:**
“See ops/architecture-v1.png (or architecture-template.txt) for the system layout.”

-**Development**

Git hooks
To enable the pre-commit policy lock check locally, run:
bash scripts/setup_hooks.sh

This configures Git to use .githooks so the policy-lock check runs on commit


