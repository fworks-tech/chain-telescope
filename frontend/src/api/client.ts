const BASE = import.meta.env.DEV ? "http://localhost:8000" : "";

export interface Snapshot {
  time_window: string;
  watchlist: string[];
  trend_filter: string;
  primary_asset: string;
  price_dates: string[];
  price_values: number[];
  price_source: string;
  kpis: Record<string, string>[];
  risk_scores: number[];
  risk_labels: string[];
  risk_colors: string[];
  alerts: string[];
  news: string[];
}

export interface PriceTrend {
  asset: string;
  dates: string[];
  prices: number[];
  trend: number[];
  source: string;
}

export interface NewsItem {
  id: string;
  source: string;
  published_at: string;
  title: string;
  url: string;
  tags: string[];
}

async function fetchJson<T>(path: string, opts?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...opts,
  });
  if (!res.ok) throw new Error(`API ${res.status}: ${res.statusText}`);
  return res.json();
}

export function getSnapshot(
  window = "30D",
  assets = "BTC",
  source = "auto",
  trend = "all"
): Promise<Snapshot> {
  const params = new URLSearchParams({ window, assets, source, trend });
  return fetchJson<Snapshot>(`/api/snapshot?${params}`);
}

export function getPriceTrend(
  asset = "BTC",
  days = 30,
  window = "30D",
  source = "auto"
): Promise<PriceTrend> {
  const params = new URLSearchParams({
    asset,
    days: String(days),
    window,
    source,
  });
  return fetchJson<PriceTrend>(`/api/price-trend?${params}`);
}

export function getNews(
  watchlist = "BTC",
  limit = 10
): Promise<NewsItem[]> {
  const params = new URLSearchParams({ watchlist, limit: String(limit) });
  return fetchJson<NewsItem[]>(`/api/news?${params}`);
}

export function getAlerts(
  window = "30D",
  assets = "BTC"
): Promise<{ alerts: string[] }> {
  const params = new URLSearchParams({ window, assets });
  return fetchJson<{ alerts: string[] }>(`/api/alerts?${params}`);
}

export function getHealth(): Promise<{ status: string }> {
  return fetchJson<{ status: string }>("/api/health");
}
