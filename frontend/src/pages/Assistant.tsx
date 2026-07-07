import ComingSoon from "../components/ComingSoon";

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
      <ComingSoon
        title="AI Assistant"
        description="Chat with an AI-powered crypto assistant that understands your watchlist, market trends, and risk profiles. The backend API endpoint is being implemented."
        icon="🤖"
      />
    </div>
  );
}
