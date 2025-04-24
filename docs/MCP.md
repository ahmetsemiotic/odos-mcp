## Model Context Protocol for Odos API

### 1. Protocol Overview
- **Name:** Odos API MCP  
- **Version:** 1.0  
- **Domain:** DeFi smart-order routing, on-chain swap assembly, router/executor lookup  

### 2. Authentication & Rate Limits
- **Authentication:** None (public REST endpoints)  
- **Headers:**  
  - `Content-Type: application/json`  
- **Rate Limits & Billing:** Governed by Odos API Pricing & Tiers  

### 3. Endpoint Definitions

#### 3.1 `POST /sor/quote/v2`
Generate a multi-token swap quote across liquidity sources.
```jsonc
Request:
{
  "chainId": 1,
  "inputTokens": [
    {
      "tokenAddress": "0x…",
      "amount": "100000" 
    }
  ],
  "outputTokens": [
    {
      "tokenAddress": "0x…",
      "proportion": 1
    }
  ],
  "slippageLimitPercent": 0.3,
  "userAddr": "0x…",
  // optional:
  "referralCode": 0,
  "disableRFQs": true,
  "compact": true
}

Response (200):
{
  "pathId": "…",      // use for /sor/assemble
  …other quote details…
}
```
- **Notes:**  
  - Paths expire in ~60 s; re-quote if expired.  

#### 3.2 `POST /sor/assemble`
Assemble the on-chain transaction data for a given quote.
```jsonc
Request:
{
  "userAddr": "0x…",
  "pathId": "…",       
  "simulate": false    // true = skip your own gas‐estimate
}

Response (200):
{
  "transaction": {
    "to":       "0x…",     // router address
    "data":     "0x…",     // call data
    "value":    "…",
    "gasLimit": 200000,    // optional
    …EIP-1559 or legacy fields…
  }
}
```
- **Best Practice:**  
  - Do **not** edit `transaction.data` manually—use it as-is.

#### 3.3 `GET /info/router/{version}/{chain_id}`
Lookup the on-chain router contract address.
```text
GET /info/router/v2/1  →  { "address": "0x…" }
```

#### 3.4 `GET /info/executor/{version}/{chain_id}`
Lookup the executor contract address (for agent/meta-tx).
```text
GET /info/executor/v2/1  →  { "address": "0x…" }
```

### 4. Error Handling
All non-200 responses return JSON:
```json
{ "code": 4003, "message": "INVALID_OUTPUT_TOKENS" }
```
**Error categories:**
- **1XXX** – General API  
- **2XXX** – Quote path errors  
- **3XXX** – Internal service errors  
- **4XXX** – Validation/request errors  
- **41XX** – Assembly errors  
- **42XX** – Swap errors  

**Agent Retry Logic:**
- Retry on transient network errors or 5XX  
- Surface 4XXX errors to user (“Invalid request”, “No viable path”, etc.)

### 5. Agent Workflow Patterns
1. **Receive user intent.**  
2. **Quote:** `POST /sor/quote/v2`  
3. **Validate:** if no `pathId` or `2000 NO_VIABLE_PATH`, inform user.  
4. **Assemble:** `POST /sor/assemble` with that `pathId`.  
5. **Execute:** sign & send the returned transaction.  
6. **Confirm:** poll chain for receipt.

### 6. Example Agent Dialogue
> **User:** “Swap 1 ETH → USDC on Mainnet with 0.5% slippage.”  
> **Agent (internally):**  
> ```text
> POST /sor/quote/v2 { chainId:1, inputTokens:[…], outputTokens:[…], slippageLimitPercent:0.5, userAddr:… }
> → { pathId: "abc123", … }
> POST /sor/assemble { userAddr:…, pathId:"abc123", simulate:false }
> → { transaction: { to:"0x…", data:"0x…", value:"0" } }
> ```  
> **Agent (to user):** “Here’s a signed transaction ready for you to broadcast.”

### 7. Notes & Best Practices
- **No manual call-data edits**—always use `assemble` output.  
- **Path validity** is ~60 s—re-quote if delayed.  
- **Gas estimation:** use `simulate:true` to let Odos estimate it.  
- **Contract integration:** for C-to-C calls, use `data` on the router address.  
- **Versioning:** confirm router/executor via `/info` before sending.

---


