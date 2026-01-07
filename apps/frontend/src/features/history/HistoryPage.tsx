import { useEffect, useState } from "react";
import { fetchHistory, HistoryItem } from "./historyApi.ts";
import "./HistoryPage.css";

export default function HistoryPage() {
  const [items, setItems] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    fetchHistory()
      .then((data) => {
        // Safety check: ensure data is an array
        if (Array.isArray(data)) {
          setItems(data);
        } else {
          console.error("fetchHistory did not return an array:", data);
          setItems([]);
          setError("Invalid data format received");
        }
      })
      .catch((err) => {
        console.error("Failed to fetch history:", err);
        setError("Failed to load history");
        setItems([]);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return (
    <div className="history-container">
      <h2>History</h2>

      {loading && (
        <div className="loading-state">
          <div className="spinner-large"></div>
          <p>Loading history...</p>
        </div>
      )}

      {error && (
        <div className="error-state">
          <p>⚠️ {error}</p>
        </div>
      )}

      {!loading && !error && items.length === 0 && (
        <div className="empty-state">
          <p>No history yet. Start segmenting some text!</p>
        </div>
      )}

      {!loading && !error && items.length > 0 && (
        <div className="history-table-wrapper">
          <table className="history-table">
            <thead>
              <tr>
                <th>Input</th>
                <th>Output</th>
              </tr>
            </thead>
            <tbody>
              {items.map((i) => (
                <tr key={i.id}>
                  <td>{i.input}</td>
                  <td>{i.output}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}