# test_swap.py
from odos_client import quote, assemble

# Base Mainnet parameters
CHAIN_ID = 8453  # Base chain ID :contentReference[oaicite:0]{index=0}
USDC     = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"  # USDC on Base :contentReference[oaicite:1]{index=1}
WETH     = "0x4200000000000000000000000000000000000006"  # WETH on Base :contentReference[oaicite:2]{index=2}

# 1 USDC → WETH (USDC has 6 decimals)
input_tokens  = [{"tokenAddress": USDC, "amount": str(1_000_000)}]
output_tokens = [{"tokenAddress": WETH, "proportion": 1}]

try:
    print("Requesting quote for 1 USDC → WETH on Base…")
    quote_resp = quote(
        chain_id=CHAIN_ID,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        slippage_pct=0.5
    )
    print("QUOTE →", quote_resp)

    print("Assembling transaction (simulate gas estimate)…")
    assemble_resp = assemble(quote_resp["pathId"], simulate=True)
    print("ASSEMBLE →", assemble_resp)

except Exception as e:
    if hasattr(e, "response"):
        print("Error response body:", e.response.text)
    raise
