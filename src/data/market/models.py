from pydantic import BaseModel, Field


class MarketSeries(BaseModel):
  asset: str
  dates: list[str]
  prices: list[float]
  source: str = "mock"


class MarketConfig(BaseModel):
  provider: str = Field(default="auto")
  binance_base_url: str = Field(default="https://api.binance.com")
  coingecko_base_url: str = Field(default="https://api.coingecko.com/api/v3")
  request_timeout_seconds: float = Field(default=10.0)
