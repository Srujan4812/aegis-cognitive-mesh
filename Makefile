# ACM Makefile

.PHONY: policy-hash policy-lock policy-validate verify pass fail clean simulate simulate-example verify-sim verify-sim-example

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

# Simulator shortcuts (Day 10)
simulate:
	@./scripts/simulate_plan.sh $(SNAPSHOT) $(PLAN)

simulate-example:
	@./scripts/simulate_plan.sh twin_snapshot.json plan_example.json

# Verify → Simulate chain (Day 10)
verify-sim:
	@./scripts/verify_then_simulate.sh $(PLAN) $(SNAPSHOT)

verify-sim-example:
	@./scripts/verify_then_simulate.sh plan_pass.json twin_snapshot.json

# Housekeeping
clean:
	@find . -name "__pycache__" -type d -prune -exec rm -rf {} + 2>/dev/null || true

.PHONY: artifact artifact-example

artifact:
	@./scripts/verify_then_simulate_json.py $(PLAN) $(SNAPSHOT)

artifact-example:
	@./scripts/verify_then_simulate_json.py plan_pass.json twin_snapshot.json

