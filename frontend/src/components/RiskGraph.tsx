import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Cell,
} from "recharts";

interface RiskGraphProps {
  scores: number[];
  labels: string[];
  colors: string[];
}

export default function RiskGraph({
  scores,
  labels,
  colors,
}: RiskGraphProps) {
  if (!scores || scores.length === 0) {
    return (
      <div
        style={{
          height: 250,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: "#888",
          background: "#1a1a2e",
          borderRadius: 8,
          border: "1px solid #2a2a4a",
        }}
      >
        No risk data available
      </div>
    );
  }

  const data = labels.map((label, i) => ({
    label,
    score: scores[i] ?? 0,
    color: colors[i] ?? "#666",
  }));

  return (
    <div
      style={{
        background: "#1a1a2e",
        borderRadius: 8,
        padding: 16,
        border: "1px solid #2a2a4a",
      }}
    >
      <div style={{ fontWeight: 600, marginBottom: 12, fontSize: 18 }}>
        Risk Analysis
      </div>
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={data} layout="vertical" margin={{ left: 80 }}>
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="#2a2a4a"
            horizontal={false}
          />
          <XAxis
            type="number"
            domain={[0, 100]}
            stroke="#666"
            tick={{ fontSize: 11 }}
          />
          <YAxis
            type="category"
            dataKey="label"
            stroke="#ccc"
            tick={{ fontSize: 12 }}
            width={80}
          />
          <Tooltip
            contentStyle={{
              background: "#0f0f23",
              border: "1px solid #2a2a4a",
              borderRadius: 6,
              fontSize: 13,
            }}
            formatter={(value) => [`${value}/100`, "Risk Score"]}
          />
          <Bar dataKey="score" radius={[0, 4, 4, 0]} barSize={20}>
            {data.map((entry, i) => (
              <Cell key={i} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
