import { useEffect, useState } from "react";
import { getSnapshot } from "../api/client";
import type { Snapshot } from "../api/client";
import KpiRow from "../components/KpiRow";
import PriceTrendChart from "../components/PriceTrendChart";
import NewsFeed from "../components/NewsFeed";
import RiskGraph from "../components/RiskGraph";
import AlertsPanel from "../components/AlertsPanel";

export default function Dashboard() {
  const [snap, setSnap] = useState<Snapshot | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getSnapshot()
      .then(setSnap)
      .catch((e) => setError(e.message));
  }, []);

  if (error) {
    return (
      <div style={{ color: "#ff6b6b", textAlign: "center", padding: 48 }}>
        Failed to load dashboard: {error}
      </div>
    );
  }

  if (!snap) {
    return (
      <div style={{ color: "#888", textAlign: "center", padding: 48 }}>
        Loading dashboard...
      </div>
    );
  }

  const newsItems = snap.news.map((title) => ({
    id: title,
    source: "",
    published_at: new Date().toISOString(),
    title,
    url: "#",
    tags: [] as string[],
  }));

  return (
    <div>
      <div style={{ marginBottom: 24 }}>
        <h1 style={{ margin: 0, fontSize: 24, fontWeight: 700 }}>Dashboard</h1>
        <p style={{ margin: "4px 0 0", color: "#888", fontSize: 13 }}>
          {snap.time_window} · {snap.watchlist.join(", ")} ·{" "}
          {snap.trend_filter}
        </p>
      </div>

      <div style={{ marginBottom: 24 }}>
        <KpiRow kpis={snap.kpis} />
      </div>

      <div style={{ marginBottom: 24 }}>
        <PriceTrendChart
          dates={snap.price_dates}
          prices={snap.price_values}
          trend={[]}
          asset={snap.primary_asset}
          source={snap.price_source}
        />
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>
        <div>
          <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 12 }}>
            Risk Overview
          </h2>
          <RiskGraph
            scores={snap.risk_scores}
            labels={snap.risk_labels}
            colors={snap.risk_colors}
          />
        </div>
        <div>
          <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 12 }}>
            Alerts
          </h2>
          <AlertsPanel alerts={snap.alerts} />
        </div>
      </div>

      <div style={{ marginTop: 24 }}>
        <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 12 }}>
          Latest News
        </h2>
        <NewsFeed items={newsItems} />
      </div>
    </div>
  );
}
