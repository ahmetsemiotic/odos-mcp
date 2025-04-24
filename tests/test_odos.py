# tests/test_odos.py
import pytest
from odos_client import quote, assemble, get_router, get_executor

def test_full_quote_assemble_flow():
    q = quote(
        chain_id=1,
        input_tokens=[{"tokenAddress":"0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2","amount":"1000000000000000000"}],
        output_tokens=[{"tokenAddress":"0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48","proportion":1}],
        slippage_pct=0.5
    )
    assert "pathId" in q

    a = assemble(q["pathId"], simulate=True)
    assert "transaction" in a
    assert a["transaction"]["to"].startswith("0x")

def test_invalid_quote_errors():
    with pytest.raises(Exception):
        quote(chain_id="not-int", input_tokens=[], output_tokens=[], slippage_pct=0.5)

@pytest.mark.parametrize("version,chain", [("v2", 1), ("v0", 1)])
def test_info_endpoints(version, chain):
    if version == "v2":
        r = get_router(version, chain)
        assert "address" in r
    else:
        with pytest.raises(Exception):
            get_router(version, chain)


