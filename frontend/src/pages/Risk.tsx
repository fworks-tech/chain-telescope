import { useEffect, useState } from "react";
import { getSnapshot } from "../api/client";
import type { Snapshot } from "../api/client";
import RiskGraph from "../components/RiskGraph";

export default function RiskPage() {
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
        Failed to load risk data: {error}
      </div>
    );
  }

  if (!snap) {
    return (
      <div style={{ color: "#888", textAlign: "center", padding: 48 }}>
        Loading risk analysis...
      </div>
    );
  }

  return (
    <div>
      <div style={{ marginBottom: 24 }}>
        <h1 style={{ margin: 0, fontSize: 24, fontWeight: 700 }}>
          Risk Analysis
        </h1>
        <p style={{ margin: "4px 0 0", color: "#888", fontSize: 13 }}>
          {snap.time_window} · {snap.watchlist.join(", ")}
        </p>
      </div>
      <div style={{ maxWidth: 600 }}>
        <RiskGraph
          scores={snap.risk_scores}
          labels={snap.risk_labels}
          colors={snap.risk_colors}
        />
      </div>
      {snap.alerts.length > 0 && (
        <div style={{ marginTop: 32 }}>
          <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 12 }}>
            Active Alerts
          </h2>
          {snap.alerts.map((alert, i) => (
            <div
              key={i}
              style={{
                padding: "10px 14px",
                marginBottom: 6,
                background: "#1a1a2e",
                borderRadius: 8,
                border: "1px solid #2a2a4a",
                fontSize: 13,
                color: "#ffd93d",
              }}
            >
              {alert}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
