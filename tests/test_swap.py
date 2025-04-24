# test_swap.py
from odos_client import quote, assemble

# Base parameters
CHAIN_ID = 8453
USDC     = "0x7F5c764cBc14f9669B88837ca1490f5aF2Ea8c4"
WETH     = "0x4200000000000000000000000000000000000006"

# 1 USDC → WETH (1e6 units for USDC)
input_tokens  = [{"tokenAddress": USDC, "amount": str(1_000_000)}]
output_tokens = [{"tokenAddress": WETH, "proportion": 1}]

try:
    # 1) Get a quote
    quote_resp = quote(
        chain_id=CHAIN_ID,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        slippage_pct=0.5
    )
    print("QUOTE →", quote_resp)

    # 2) Assemble the transaction (simulate gas estimate)
    assemble_resp = assemble(quote_resp["pathId"], simulate=True)
    print("ASSEMBLE →", assemble_resp)

except Exception as e:
    # Print the raw response body if available
    if hasattr(e, 'response'):
        print("Error response body:", e.response.text)
    raise
