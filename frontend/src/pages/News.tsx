import { useEffect, useState } from "react";
import { getNews } from "../api/client";
import type { NewsItem } from "../api/client";
import NewsFeed from "../components/NewsFeed";

export default function NewsPage() {
  const [items, setItems] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getNews("BTC,ETH,SOL", 20)
      .then(setItems)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <div style={{ marginBottom: 24 }}>
        <h1 style={{ margin: 0, fontSize: 24, fontWeight: 700 }}>News Feed</h1>
        <p style={{ margin: "4px 0 0", color: "#888", fontSize: 13 }}>
          Latest crypto news from RSS/Atom feeds
        </p>
      </div>
      {loading && (
        <div style={{ color: "#888", textAlign: "center", padding: 48 }}>
          Loading news...
        </div>
      )}
      {error && (
        <div style={{ color: "#ff6b6b", textAlign: "center", padding: 48 }}>
          Failed to load news: {error}
        </div>
      )}
      {!loading && !error && <NewsFeed items={items} />}
    </div>
  );
}
