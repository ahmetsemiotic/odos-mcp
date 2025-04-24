```markdown
# Odos MCP Test Harness (Beta)

> **⚠️ WARNING:** This is a **beta** version of the Odos Model Context Protocol (MCP) harness.  
> Use this code **at your own risk**. It may change without notice, and is provided “as-is” with no warranty.

## Overview
This repository contains a minimal Python test harness and documentation for interacting with the Odos smart-order-routing API.  
It implements and verifies the Model Context Protocol (MCP) for:
- Quoting swaps (`POST /sor/quote/v2`)  
- Assembling transactions (`POST /sor/assemble`)  
- Looking up router/executor contracts (`GET /info/router/{version}/{chain_id}`, `GET /info/executor/{version}/{chain_id}`)

## Contents
```
docs/
  └── MCP.md           ← Full MCP specification
odo​s_client.py        ← Python client stubs
quote_only.py         ← Quick script to fetch a quote
test_swap.py          ← Example swap (USDC → WETH on Base)
tests/                ← pytest suite validating all MCP steps
config.py             ← Test parameters (chainId, userAddr, etc.)
requirements.txt      ← Python dependencies
README.md             ← (this file)
```

## Getting Started

1. **Clone & Enter Directory**  
   ```bash
   git clone https://github.com/YourUserName/odos-mcp.git
   cd odos-mcp
   ```

2. **Create & Activate Virtual Environment**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Tests**  
   ```bash
   pytest -q
   ```

5. **Fetch a Quote**  
   ```bash
   python quote_only.py
   ```

## Usage Examples

### Python
```python
from odos_client import quote, assemble

# 1. Get a quote
resp = quote(
    chain_id=8453,
    input_tokens=[{"tokenAddress":"0x...","amount":"1000000"}],
    output_tokens=[{"tokenAddress":"0x...","proportion":1}],
    slippage_pct=0.5
)
print(resp)

# 2. Assemble transaction (simulate gas estimation)
tx = assemble(resp["pathId"], simulate=True)
print(tx)
```

### cURL
```bash
curl -X POST https://api.odos.xyz/sor/quote/v2 \
  -H "Content-Type: application/json" \
  -d '{
    "chainId": 8453,
    "inputTokens":[{"tokenAddress":"0x...","amount":"1000000"}],
    "outputTokens":[{"tokenAddress":"0x...","proportion":1}],
    "slippageLimitPercent":0.5,
    "userAddr":"0xYourTestAddr",
    "disableRFQs":true,
    "compact":true
  }'
```

## Contributing
1. Fork & clone the repository  
2. Create a feature branch: `git checkout -b my-feature`  
3. Make your changes & add tests  
4. Commit: `git commit -m "Add awesome feature"`  
5. Push: `git push origin my-feature`  
6. Open a Pull Request

## License & Disclaimer
This code is provided under the MIT License.  
**Use it at your own risk**—the authors make no guarantees about functionality, performance, or suitability for any purpose.
```
