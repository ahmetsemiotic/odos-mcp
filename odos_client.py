# odos_client.py
import requests
from config import BASE_URL, TEST_ADDRESS

def quote(chain_id, input_tokens, output_tokens, slippage_pct):
    payload = {
        "chainId": chain_id,
        "inputTokens": input_tokens,
        "outputTokens": output_tokens,
        "slippageLimitPercent": slippage_pct,
        "userAddr": TEST_ADDRESS,
        "disableRFQs": True,
        "compact": True
    }
    resp = requests.post(f"{BASE_URL}/sor/quote/v2", json=payload)
    resp.raise_for_status()
    return resp.json()

def assemble(path_id, simulate=True):
    payload = {
        "userAddr": TEST_ADDRESS,
        "pathId": path_id,
        "simulate": simulate
    }
    resp = requests.post(f"{BASE_URL}/sor/assemble", json=payload)
    resp.raise_for_status()
    return resp.json()

def get_router(version, chain_id):
    resp = requests.get(f"{BASE_URL}/info/router/{version}/{chain_id}")
    resp.raise_for_status()
    return resp.json()

def get_executor(version, chain_id):
    resp = requests.get(f"{BASE_URL}/info/executor/{version}/{chain_id}")
    resp.raise_for_status()
    return resp.json()

