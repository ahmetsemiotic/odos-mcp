# quote_only.py
from odos_client import quote

resp = quote(
    chain_id=8453,
    input_tokens=[{
        "tokenAddress": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        "amount": "1000000"
    }],
    output_tokens=[{
        "tokenAddress": "0x4200000000000000000000000000000000000006",
        "proportion": 1
    }],
    slippage_pct=0.5
)

import json
print(json.dumps(resp, indent=2))
