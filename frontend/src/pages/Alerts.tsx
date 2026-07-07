import ComingSoon from "../components/ComingSoon";

export default function AlertsPage() {
  return (
    <div>
      <div style={{ marginBottom: 24 }}>
        <h1 style={{ margin: 0, fontSize: 24, fontWeight: 700 }}>Alerts</h1>
        <p style={{ margin: "4px 0 0", color: "#888", fontSize: 13 }}>
          Rule-driven alert engine for market conditions
        </p>
      </div>
      <ComingSoon
        title="Alerts Engine"
        description="Configure custom alert rules for price thresholds, momentum triggers, and risk conditions. Get notified when your watchlist assets cross defined boundaries."
      />
    </div>
  );
}
