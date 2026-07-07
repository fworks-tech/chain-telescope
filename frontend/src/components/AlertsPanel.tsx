interface AlertsPanelProps {
  alerts: string[];
}

const severityColor = (alert: string) => {
  const lower = alert.toLowerCase();
  if (lower.includes("high") || lower.includes("critical") || lower.includes("!!!"))
    return { bg: "#3d1a1a", border: "#ff6b6b", color: "#ff6b6b" };
  if (lower.includes("medium") || lower.includes("!!"))
    return { bg: "#3d2e1a", border: "#ffd93d", color: "#ffd93d" };
  return { bg: "#1a2e1a", border: "#4ecca3", color: "#4ecca3" };
};

export default function AlertsPanel({ alerts }: AlertsPanelProps) {
  if (!alerts || alerts.length === 0) {
    return (
      <div style={{ color: "#888", textAlign: "center", padding: 24 }}>
        No alerts at this time.
      </div>
    );
  }

  return (
    <div>
      {alerts.map((alert, i) => {
        const sev = severityColor(alert);
        return (
          <div
            key={i}
            style={{
              padding: "10px 14px",
              marginBottom: 6,
              background: sev.bg,
              borderRadius: 8,
              border: `1px solid ${sev.border}`,
              fontSize: 13,
              color: sev.color,
            }}
          >
            {alert}
          </div>
        );
      })}
    </div>
  );
}
