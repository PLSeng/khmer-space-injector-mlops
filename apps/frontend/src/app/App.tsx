import { useState } from "react";
import SegmentPage from "../features/segment/Segment";
import HistoryPage from "../features/history/HistoryPage";
import "./App.css";

export default function App() {
  const [showHistory, setShowHistory] = useState(false);

  return (
    <>
      <SegmentPage />
      
      {/* History Toggle Button */}
      <div className="history-button-container">
        <button 
          className="history-toggle-button" 
          onClick={() => setShowHistory(!showHistory)}
        >
          <span className="history-icon">📜</span>
          <span>{showHistory ? "Hide History" : "View History"}</span>
        </button>
      </div>

      {/* History Section - Only shows when button is clicked */}
      {showHistory && (
        <div className="history-section">
          <HistoryPage />
        </div>
      )}
    </>
  );
}