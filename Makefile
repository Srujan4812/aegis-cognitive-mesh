.PHONY: policy-hash policy-lock

policy-hash:
	@python3 scripts/hash_policy.py

policy-lock:
	@HASH=$$(python3 scripts/hash_policy.py); \
	printf "policy_sha256: $$HASH\n" > policies/policy.lock; \
	echo "Updated policies/policy.lock to $$HASH"
