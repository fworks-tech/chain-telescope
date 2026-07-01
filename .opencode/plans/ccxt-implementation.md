# ccxt Exchange Adapter — Implementation Plan

**Issue:** #77  
**Branch:** `feat/002-ccxt-exchange` (from `main`)

## Goal

Replace three custom exchange adapters (`binance.py`, `coingecko.py`, `coinbase.py`) with a single unified `ccxt` adapter. ccxt handles rate limits, retries, unified response format, and 100+ exchanges out of the box.

## Current vs Target Architecture

### Current
```
fetch_price_trend()
  → _fetch_provider_series(name, asset, days)
    → binance.fetch_binance_series()     # custom requests.get + parsing
    → coingecko.fetch_coingecko_series() # custom requests.get + parsing  
    → coinbase.fetch_coinbase_series()   # custom requests.get + parsing
```

### Target
```
fetch_price_trend()
  → _fetch_provider_series(name, asset, days)
    → ccxt_adapter.fetch_ccxt_series()   # unified ccxt.exchange().fetch_ohlcv()
```

## Steps

### 1. Add ccxt to requirements.txt
```python
ccxt>=4.3.0
```

### 2. Create `src/data/market/ccxt_adapter.py`

The adapter maps asset symbols to ccxt exchange IDs and fetches OHLCV data:

```python
import ccxt
from datetime import datetime
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

EXCHANGE_MAP = {
    "binance": ccxt.binance,
    "coinbase": ccxt.coinbase,
    "coingecko": ccxt.coingecko,
}

SYMBOL_MAP = {
    "binance": "BTC/USDT",
    "coinbase": "BTC/USD",
    "coingecko": "BTC/USD",
}

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def fetch_ccxt_series(exchange_name: str, asset: str, days: int):
    exchange_class = EXCHANGE_MAP.get(exchange_name)
    if not exchange_class:
        return None
    
    symbol = SYMBOL_MAP.get(exchange_name, f"{asset}/USDT")
    exchange = exchange_class({"enableRateLimit": True})
    
    # ccxt.fetch_ohlcv returns [[timestamp, open, high, low, close, volume], ...]
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe="1d", limit=max(days, 1))
    if not ohlcv:
        return None
    
    dates = [datetime.fromtimestamp(row[0] / 1000) for row in ohlcv]
    prices = [float(row[4]) for row in ohlcv]  # close price
    return dates, prices, exchange_name
```

### 3. Update `src/data/market/service.py`

Replace the direct imports and `_fetch_provider_series()` to use ccxt:

```python
from src.data.market.ccxt_adapter import fetch_ccxt_series

# Remove imports of binance, coinbase, coingecko

def _fetch_provider_series(provider: str, asset: str, days: int):
    if provider in ("binance", "coingecko", "coinbase"):
        return fetch_ccxt_series(provider, asset, days)
    return None
```

Remove the old adapter files: `binance.py`, `coingecko.py`, `coinbase.py`.

### 4. Update `src/data/assets.py`

The symbol mappings (`BINANCE_SYMBOLS`, `COINBASE_PRODUCTS`, `COINGECKO_IDS`) are no longer needed by the adapter. They can be removed or kept for other purposes (they are referenced in `config.py` and `service.py` imports).

Keep them for now — they may be useful for display/metadata even if not used by ccxt.

### 5. Update `src/data/market/config.py`

Remove provider-specific base URL configs since ccxt manages its own endpoints:

```python
def load_market_config() -> MarketConfig:
    return MarketConfig(
        provider=os.getenv("MARKET_PROVIDER", "auto"),
        request_timeout_seconds=timeout,
    )
```

Update `MarketConfig` model in `models.py` to remove `binance_base_url` and `coingecko_base_url`.

### 6. Update tests

**Keep existing tests that mock adapters** — they mock at the service level, so they still work.

**Add new tests for ccxt_adapter.py:**
- `test_fetch_ccxt_series_returns_ohlcv` — mock ccxt exchange, verify shape
- `test_fetch_ccxt_series_unknown_exchange` — returns None
- `test_fetch_ccxt_series_retries_on_failure` — verify tenacity retry

**Remove tests that directly test old adapters:**
- `test_retry.py` currently tests `fetch_binance_series` etc. directly. These need updating:
  ```python
  @patch("ccxt.binance")
  def test_fetch_ccxt_series_retries(self, mock_binance_class):
      mock_exchange = mock_binance_class.return_value
      mock_exchange.fetch_ohlcv.side_effect = [
          ccxt.NetworkError("timeout"),
          ccxt.NetworkError("timeout"),
          [[1715683200000, 100, 101, 99, 100.5, 1000]],
      ]
      result = fetch_ccxt_series("binance", "BTC", 30)
      self.assertIsNotNone(result)
      self.assertEqual(mock_exchange.fetch_ohlcv.call_count, 3)
  ```

### 7. Verify quality gates

```powershell
pip install ccxt
python -m ruff check app.py src tests
python -m ruff format --check app.py src tests
python -m unittest discover -s tests -p 'test_*.py' -v
```

### 8. Clean up dead code

After verifying everything works:
- Delete `src/data/market/binance.py`
- Delete `src/data/market/coingecko.py`
- Delete `src/data/market/coinbase.py`
- Remove unused imports in `service.py`, `config.py`, `models.py`

## Rollback

If ccxt causes issues, revert is simple:
1. `git revert <commit>`
2. Old adapters are still on disk until Step 8 deletes them

## Files changed

| File | Change |
|------|--------|
| `requirements.txt` | Add `ccxt>=4.3.0` |
| `src/data/market/ccxt_adapter.py` | **New** — unified adapter |
| `src/data/market/service.py` | Replace imports + `_fetch_provider_series` |
| `src/data/market/models.py` | Remove provider-specific URL fields |
| `src/data/market/config.py` | Simplify config |
| `binance.py`, `coingecko.py`, `coinbase.py` | **Delete** (after verification) |
| `tests/test_retry.py` | Rewrite to test ccxt instead of old adapters |
| `tests/test_m4_modules.py` | Update mock paths if needed |
