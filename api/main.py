from fastapi import FastAPI
from hub.policy_hash import policy_hash

app = FastAPI(title="ACM Hub")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/policy/hash")
def get_policy_hash():
    return {"hash": policy_hash("policies/base.yaml")}
