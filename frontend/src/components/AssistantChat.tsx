import { useState } from "react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function AssistantChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Hi! I'm the ChainTelescope assistant. Ask me about crypto markets, trends, or any asset in your watchlist.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;
    const userMsg: Message = { role: "user", content: input.trim() };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("/api/assistant", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userMsg.content,
          history: messages.slice(-6),
        }),
      });
      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.reply || data.message || "No response." },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Sorry, I'm having trouble connecting. Please try again." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        background: "#1a1a2e",
        borderRadius: 8,
        border: "1px solid #2a2a4a",
        display: "flex",
        flexDirection: "column",
        height: 500,
      }}
    >
      <div style={{ padding: "12px 16px", borderBottom: "1px solid #2a2a4a", fontWeight: 600 }}>
        AI Assistant
      </div>
      <div style={{ flex: 1, overflowY: "auto", padding: 16, display: "flex", flexDirection: "column", gap: 12 }}>
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              alignSelf: msg.role === "user" ? "flex-end" : "flex-start",
              maxWidth: "80%",
              padding: "10px 14px",
              borderRadius: 12,
              fontSize: 14,
              lineHeight: 1.5,
              background: msg.role === "user" ? "#4ecca3" : "#2a2a4a",
              color: msg.role === "user" ? "#0f0f23" : "#eee",
            }}
          >
            {msg.content}
          </div>
        ))}
        {loading && (
          <div style={{ alignSelf: "flex-start", color: "#888", fontSize: 13 }}>
            Thinking...
          </div>
        )}
      </div>
      <div style={{ padding: 12, borderTop: "1px solid #2a2a4a", display: "flex", gap: 8 }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Ask about crypto markets..."
          style={{
            flex: 1,
            background: "#0f0f23",
            border: "1px solid #2a2a4a",
            borderRadius: 6,
            padding: "10px 14px",
            color: "#eee",
            fontSize: 14,
            outline: "none",
          }}
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          style={{
            background: loading ? "#2a2a4a" : "#4ecca3",
            border: "none",
            borderRadius: 6,
            padding: "10px 20px",
            color: loading ? "#666" : "#0f0f23",
            fontWeight: 600,
            cursor: loading ? "not-allowed" : "pointer",
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
}
