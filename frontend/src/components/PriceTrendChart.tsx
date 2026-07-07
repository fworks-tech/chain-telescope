import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

interface PriceTrendChartProps {
  dates: string[];
  prices: number[];
  trend: number[];
  asset: string;
  source: string;
}

export default function PriceTrendChart({
  dates,
  prices,
  trend,
  asset,
  source,
}: PriceTrendChartProps) {
  if (!dates || dates.length === 0) {
    return (
      <div
        style={{
          height: 300,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: "#888",
          background: "#1a1a2e",
          borderRadius: 8,
          border: "1px solid #2a2a4a",
        }}
      >
        No price data available
      </div>
    );
  }

  const data = dates.map((d, i) => ({
    date: new Date(d).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
    }),
    price: prices[i] ?? 0,
    trend: trend[i] ?? 0,
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
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginBottom: 12,
        }}
      >
        <span style={{ fontWeight: 600, fontSize: 18 }}>
          {asset} Price Trend
        </span>
        <span style={{ fontSize: 12, color: "#888" }}>Source: {source}</span>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <AreaChart data={data}>
          <defs>
            <linearGradient id="priceGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#4ecca3" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#4ecca3" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="#2a2a4a"
            vertical={false}
          />
          <XAxis
            dataKey="date"
            stroke="#666"
            tick={{ fontSize: 11 }}
            interval="preserveStartEnd"
          />
          <YAxis
            stroke="#666"
            tick={{ fontSize: 11 }}
            domain={["auto", "auto"]}
            tickFormatter={(v) => `$${v.toLocaleString()}`}
          />
          <Tooltip
            contentStyle={{
              background: "#0f0f23",
              border: "1px solid #2a2a4a",
              borderRadius: 6,
              fontSize: 13,
            }}
            labelStyle={{ color: "#ccc" }}
          />
          <Area
            type="monotone"
            dataKey="price"
            stroke="#4ecca3"
            fill="url(#priceGrad)"
            strokeWidth={2}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
