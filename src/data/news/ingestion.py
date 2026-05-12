import hashlib
import os
from datetime import datetime, timezone

import feedparser
from dotenv import load_dotenv

from src.data.mock_market import news_snapshot
from src.data.news.models import FeedItem

load_dotenv()

DEFAULT_FEEDS = [
  "https://www.coindesk.com/arc/outboundfeeds/rss/",
  "https://cointelegraph.com/rss",
]

FALLBACK_ITEMS = [
  FeedItem(
    id="fallback-etf",
    source="mock",
    published_at=datetime.now(timezone.utc),
    title="ETF flows rebound",
    url="https://example.com/etf-flows",
    tags=["BTC", "ETF"],
  ),
  FeedItem(
    id="fallback-sol",
    source="mock",
    published_at=datetime.now(timezone.utc),
    title="Layer-1 activity rotates to SOL",
    url="https://example.com/sol-activity",
    tags=["SOL"],
  ),
  FeedItem(
    id="fallback-reserves",
    source="mock",
    published_at=datetime.now(timezone.utc),
    title="Exchange reserves decline",
    url="https://example.com/exchange-reserves",
    tags=["BTC", "ETH"],
  ),
]


def _feed_urls():
  configured = os.getenv("NEWS_FEED_URLS", "")
  if configured.strip():
    return [url.strip() for url in configured.split(",") if url.strip()]
  return DEFAULT_FEEDS


def _item_id(source: str, title: str, url: str) -> str:
  digest = hashlib.sha256(f"{source}|{title}|{url}".encode("utf-8")).hexdigest()
  return digest[:16]


def _parse_feed(url: str) -> list[FeedItem]:
  parsed = feedparser.parse(url)
  items = []
  for entry in parsed.entries[:20]:
    title = getattr(entry, "title", "").strip()
    link = getattr(entry, "link", "").strip()
    if not title:
      continue
    published = getattr(entry, "published_parsed", None)
    published_at = datetime(*published[:6], tzinfo=timezone.utc) if published else datetime.now(timezone.utc)
    tags = [tag.term for tag in getattr(entry, "tags", []) if getattr(tag, "term", None)]
    items.append(
      FeedItem(
        id=_item_id(url, title, link or title),
        source=url,
        published_at=published_at,
        title=title,
        url=link or url,
        tags=tags,
      )
    )
  return items


def _dedupe_items(items: list[FeedItem]) -> list[FeedItem]:
  seen = set()
  deduped = []
  for item in items:
    key = (item.title.lower(), item.url)
    if key in seen:
      continue
    seen.add(key)
    deduped.append(item)
  return deduped


def _filter_by_watchlist(items: list[FeedItem], watchlist: list[str] | None) -> list[FeedItem]:
  if not watchlist:
    return items
  lowered = [asset.lower() for asset in watchlist]
  filtered = [
    item for item in items
    if any(asset in item.title.lower() or asset in [tag.lower() for tag in item.tags] for asset in lowered)
  ]
  return filtered or items


def load_news_items(watchlist: list[str] | None = None) -> list[FeedItem]:
  collected: list[FeedItem] = []
  for url in _feed_urls():
    try:
      collected.extend(_parse_feed(url))
    except Exception:
      continue

  if not collected:
    collected = FALLBACK_ITEMS.copy()
    if watchlist:
      filtered = _filter_by_watchlist(collected, watchlist)
      if filtered:
        collected = filtered
    return _dedupe_items(collected)

  collected = _dedupe_items(collected)
  collected = _filter_by_watchlist(collected, watchlist)
  if not collected:
    collected = [
      FeedItem(
        id=_item_id("mock", line, line),
        source="mock",
        published_at=datetime.now(timezone.utc),
        title=line,
        url="https://example.com/news",
        tags=watchlist or [],
      )
      for line in news_snapshot()
    ]
  return collected
