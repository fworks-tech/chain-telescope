import { NavLink, Outlet } from "react-router-dom";

const links = [
  { to: "/", label: "Dashboard" },
  { to: "/news", label: "News" },
  { to: "/risk", label: "Risk" },
  { to: "/alerts", label: "Alerts" },
  { to: "/assistant", label: "Assistant" },
  { to: "/newsletter", label: "Newsletter" },
];

export default function Layout() {
  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#0f0f23",
        color: "#eee",
        fontFamily:
          '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      }}
    >
      <nav
        style={{
          display: "flex",
          alignItems: "center",
          gap: 24,
          padding: "12px 24px",
          borderBottom: "1px solid #2a2a4a",
          background: "#1a1a2e",
        }}
      >
        <span style={{ fontWeight: 700, fontSize: 18, color: "#4ecca3" }}>
          ChainTelescope
        </span>
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            end={link.to === "/"}
            style={({ isActive }) => ({
              color: isActive ? "#4ecca3" : "#888",
              textDecoration: "none",
              fontSize: 14,
              fontWeight: isActive ? 600 : 400,
              borderBottom: isActive
                ? "2px solid #4ecca3"
                : "2px solid transparent",
              paddingBottom: 2,
            })}
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
      <div
        style={{
          background: "#1a1a2e",
          padding: "8px 24px",
          borderBottom: "1px solid #2a2a4a",
          fontSize: 12,
          color: "#666",
          display: "flex",
          gap: 16,
          alignItems: "center",
        }}
      >
        <span style={{ color: "#ffd93d" }}>⚙</span>
        Sidebar filters (time window, watchlist, source, trend) coming soon
      </div>
      <main style={{ padding: 24, maxWidth: 1200, margin: "0 auto" }}>
        <Outlet />
      </main>
    </div>
  );
}
