import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./Layout";
import Dashboard from "./pages/Dashboard";
import NewsPage from "./pages/News";
import RiskPage from "./pages/Risk";
import AlertsPage from "./pages/Alerts";
import AssistantPage from "./pages/Assistant";
import NewsletterPage from "./pages/Newsletter";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="news" element={<NewsPage />} />
          <Route path="risk" element={<RiskPage />} />
          <Route path="alerts" element={<AlertsPage />} />
          <Route path="assistant" element={<AssistantPage />} />
          <Route path="newsletter" element={<NewsletterPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
