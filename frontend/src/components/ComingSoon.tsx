interface ComingSoonProps {
  title: string;
  description?: string;
  icon?: string;
}

export default function ComingSoon({
  title,
  description,
  icon = "🚧",
}: ComingSoonProps) {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "64px 24px",
        background: "#1a1a2e",
        borderRadius: 12,
        border: "1px dashed #2a2a4a",
        textAlign: "center",
      }}
    >
      <div style={{ fontSize: 48, marginBottom: 16 }}>{icon}</div>
      <h2
        style={{
          fontSize: 22,
          fontWeight: 600,
          color: "#eee",
          margin: "0 0 8px",
        }}
      >
        {title}
      </h2>
      <p style={{ color: "#888", fontSize: 14, maxWidth: 400, margin: 0 }}>
        {description || `The ${title} feature is under development and will be available soon.`}
      </p>
    </div>
  );
}
