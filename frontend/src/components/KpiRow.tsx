interface KpiRowProps {
  kpis: Record<string, string>[];
}

export default function KpiRow({ kpis }: KpiRowProps) {
  if (!kpis || kpis.length === 0) return null;
  return (
    <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
      {kpis.map((kpi, i) => {
        const key = Object.keys(kpi)[0];
        const val = kpi[key];
        const isUp = val.startsWith("+");
        return (
          <div
            key={i}
            style={{
              flex: "1 0 180px",
              background: "#1a1a2e",
              borderRadius: 8,
              padding: "12px 16px",
              border: "1px solid #2a2a4a",
            }}
          >
            <div style={{ fontSize: 12, color: "#888", marginBottom: 4 }}>
              {key}
            </div>
            <div
              style={{
                fontSize: 20,
                fontWeight: 700,
                color: isUp ? "#4ecca3" : "#ff6b6b",
              }}
            >
              {val}
            </div>
          </div>
        );
      })}
    </div>
  );
}
