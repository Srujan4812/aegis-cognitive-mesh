# ACM Makefile

.PHONY: policy-hash policy-lock policy-validate verify pass fail clean

# Policy utilities
policy-hash:
	@python3 scripts/hash_policy.py

policy-lock:
	@HASH=$$(python3 scripts/hash_policy.py); \
	printf "policy_sha256: $$HASH\n" > policies/policy.lock; \
	echo "Updated policies/policy.lock to $$HASH"

policy-validate:
	@python3 scripts/validate_policy.py

# Z3 verifier shortcuts (Day 9)
verify:
	@./scripts/verify_plan.sh $(PLAN)

pass:
	@./scripts/verify_plan.sh plan_pass.json

fail:
	@./scripts/verify_plan.sh plan_fail.json

# Housekeeping
clean:
	@find . -name "__pycache__" -type d -prune -exec rm -rf {} + 2>/dev/null || true
