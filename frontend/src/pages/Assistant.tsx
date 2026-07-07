import AssistantChat from "../components/AssistantChat";

export default function AssistantPage() {
  return (
    <div>
      <div style={{ marginBottom: 24 }}>
        <h1 style={{ margin: 0, fontSize: 24, fontWeight: 700 }}>
          AI Assistant
        </h1>
        <p style={{ margin: "4px 0 0", color: "#888", fontSize: 13 }}>
          Ask about crypto markets, trends, and portfolio insights
        </p>
      </div>
      <div style={{ maxWidth: 700 }}>
        <AssistantChat />
      </div>
    </div>
  );
}
