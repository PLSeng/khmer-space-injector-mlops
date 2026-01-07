import SegmentPage from "../features/segment/Segment";
import HistoryPage from "../features/history/HistoryPage";
import "./App.css";

export default function App() {
  return (
    <>
      <SegmentPage />
      
      <div className="history-section">
        <HistoryPage />
      </div>
    </>
  );
}
