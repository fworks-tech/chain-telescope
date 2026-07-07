import ComingSoon from "../components/ComingSoon";

export default function NewsletterPage() {
  return (
    <div>
      <div style={{ marginBottom: 24 }}>
        <h1 style={{ margin: 0, fontSize: 24, fontWeight: 700 }}>
          Newsletter
        </h1>
        <p style={{ margin: "4px 0 0", color: "#888", fontSize: 13 }}>
          Subscribe to daily or weekly crypto market digests
        </p>
      </div>
      <ComingSoon
        title="Newsletter Subscriptions"
        description="Sign up for automated email digests covering market trends, top movers, alert summaries, and AI-generated insights for your watchlist."
        icon="📬"
      />
    </div>
  );
}
