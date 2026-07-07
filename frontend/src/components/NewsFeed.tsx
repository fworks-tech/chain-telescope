import type { NewsItem } from "../api/client";

interface NewsFeedProps {
  items: NewsItem[];
}

export default function NewsFeed({ items }: NewsFeedProps) {
  if (!items || items.length === 0) {
    return (
      <div style={{ color: "#888", textAlign: "center", padding: 24 }}>
        No news items available.
      </div>
    );
  }

  return (
    <div>
      {items.map((item) => (
        <a
          key={item.id}
          href={item.url}
          target="_blank"
          rel="noopener noreferrer"
          style={{
            display: "block",
            padding: "12px 16px",
            marginBottom: 8,
            background: "#1a1a2e",
            borderRadius: 8,
            border: "1px solid #2a2a4a",
            textDecoration: "none",
            color: "inherit",
            transition: "border-color 0.15s",
          }}
          onMouseEnter={(e) => {
            (e.currentTarget as HTMLElement).style.borderColor = "#4ecca3";
          }}
          onMouseLeave={(e) => {
            (e.currentTarget as HTMLElement).style.borderColor = "#2a2a4a";
          }}
        >
          <div style={{ fontWeight: 500, marginBottom: 4, color: "#eee" }}>
            {item.title}
          </div>
          <div
            style={{
              display: "flex",
              gap: 8,
              fontSize: 11,
              color: "#888",
              alignItems: "center",
            }}
          >
            <span>
              {new Date(item.published_at).toLocaleDateString("en-US", {
                month: "short",
                day: "numeric",
                hour: "2-digit",
                minute: "2-digit",
              })}
            </span>
            <span>•</span>
            <span>{new URL(item.source).hostname}</span>
            {item.tags.length > 0 && (
              <>
                <span>•</span>
                {item.tags.map((tag) => (
                  <span
                    key={tag}
                    style={{
                      background: "#2a2a4a",
                      padding: "1px 6px",
                      borderRadius: 4,
                      fontSize: 10,
                      color: "#4ecca3",
                    }}
                  >
                    {tag}
                  </span>
                ))}
              </>
            )}
          </div>
        </a>
      ))}
    </div>
  );
}
