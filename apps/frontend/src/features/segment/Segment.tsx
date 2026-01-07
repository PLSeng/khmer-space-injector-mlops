import { useState } from "react";
import { segmentText } from "./segmentApi";
import "./Segment.css";

export default function SegmentPage() {
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);
  const [agreedToTerms, setAgreedToTerms] = useState(false);
  const [showTermsModal, setShowTermsModal] = useState(false);

  async function handleSegment() {
    if (!input.trim()) return alert("Please enter Khmer text");

    if (!agreedToTerms) {
      alert("Please agree to the Terms and Conditions before proceeding");
      return;
    }

    setLoading(true);
    try {
      const res = await segmentText(input);
      setOutput(res.output);
    } catch (err) {
      console.error("Segmentation error:", err);
      const message = err && (err as any).message ? (err as any).message : String(err);
      alert("Segmentation failed: " + message);
      setOutput("Error: " + message);
    } finally {
      setLoading(false);
    }
  }

  async function handleFileUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;

    const validTypes = ['text/plain', 'application/txt'];
    if (!validTypes.includes(file.type) && !file.name.endsWith('.txt')) {
      alert("Please upload a .txt file");
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      alert("File size must be less than 5MB");
      return;
    }

    try {
      const text = await file.text();
      setInput(text);
    } catch (err) {
      console.error("File reading error:", err);
      alert("Failed to read file");
    }
  }

  function clearInput() {
    setInput("");
    setOutput("");
  }

  return ( 
    <div className="segment-container">
      <div className="segment-card">
        <div className="header-section">
          <h2 className="title">Khmer Text Segmentation</h2>
          <p className="subtitle">Enter your Khmer text below or upload a file to segment it into words</p>
        </div>

        <div className="input-section">
          <div className="input-header">
            <label className="input-label">Input Text</label>
            <div className="input-actions">
              <label className="upload-button">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                Upload File
                <input 
                  type="file" 
                  accept=".txt,text/plain" 
                  onChange={handleFileUpload}
                  style={{ display: 'none' }}
                />
              </label>
              {input && (
                <button className="clear-button" onClick={clearInput}>
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                    <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                  </svg>
                  Clear
                </button>
              )}
            </div>
          </div>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            rows={6}
            className="input-textarea"
            placeholder="បញ្ចូលអត្ថបទភាសាខ្មែរ... or upload a .txt file"
          />
        </div>

        <div className="terms-section">
          <label className="terms-checkbox">
            <input
              type="checkbox"
              checked={agreedToTerms}
              onChange={(e) => setAgreedToTerms(e.target.checked)}
            />
            <span>
              I agree to the{" "}
              <button
                type="button"
                className="terms-link"
                onClick={() => setShowTermsModal(true)}
              >
                Terms and Conditions
              </button>
            </span>
          </label>
        </div>

        <button 
          onClick={handleSegment} 
          disabled={loading || !agreedToTerms}
          className={`segment-button ${loading ? 'loading' : ''} ${!agreedToTerms ? 'disabled' : ''}`}
        >
          {loading ? (
            <>
              <span className="spinner"></span>
              Processing...
            </>
          ) : (
            <>
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M10 4L10 16M4 10L16 10" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
              </svg>
              Segment Text
            </>
          )}
        </button>

        {output && (
          <div className="output-section">
            <div className="output-header">
              <label className="output-label">Result</label>
              <button 
                className="copy-button"
                onClick={() => {
                  navigator.clipboard.writeText(output);
                  alert("Copied to clipboard!");
                }}
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                  <path d="M8 4v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V7.242a2 2 0 0 0-.602-1.43L16.083 2.57A2 2 0 0 0 14.685 2H10a2 2 0 0 0-2 2z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <path d="M16 18v2a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                Copy
              </button>
            </div>
            <div className="output-box">
              {output}
            </div>
          </div>
        )}
      </div>

      {/* Terms and Conditions Modal */}
      {showTermsModal && (
        <div className="modal-overlay" onClick={() => setShowTermsModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Terms and Conditions</h3>
              <button className="modal-close" onClick={() => setShowTermsModal(false)}>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                </svg>
              </button>
            </div>
            <div className="modal-body">
              <h4>Data Usage and Privacy</h4>
              <p>
                By using this Khmer Text Segmentation service, you agree to the following terms:
              </p>
              
              <h4>1. Data Collection</h4>
              <p>
                We collect the text you submit for segmentation purposes only. This includes both manually entered text and uploaded files.
              </p>

              <h4>2. Data Usage</h4>
              <p>
                Your submitted text will be:
              </p>
              <ul>
                <li>Processed by our segmentation algorithm</li>
                <li>Stored temporarily for service delivery</li>
                <li>Used to improve our segmentation model (optional, anonymized)</li>
              </ul>

              <h4>3. Data Storage</h4>
              <p>
                We maintain a history of your segmentation requests during your session. This data is stored locally and on our servers for service improvement.
              </p>

              <h4>4. Data Security</h4>
              <p>
                We implement industry-standard security measures to protect your data. However, no method of transmission over the internet is 100% secure.
              </p>

              <h4>5. User Rights</h4>
              <p>
                You have the right to:
              </p>
              <ul>
                <li>Request deletion of your data</li>
                <li>Opt out of data collection for model improvement</li>
                <li>Access your stored data</li>
              </ul>

              <h4>6. Limitations</h4>
              <p>
                This service is provided "as is" without warranties. We are not responsible for:
              </p>
              <ul>
                <li>Accuracy of segmentation results</li>
                <li>Loss of data due to technical issues</li>
                <li>Misuse of segmented content</li>
              </ul>

              <h4>7. Changes to Terms</h4>
              <p>
                We reserve the right to modify these terms at any time. Continued use of the service constitutes acceptance of updated terms.
              </p>

              <p className="terms-footer">
                Last updated: January 7, 2026
              </p>
            </div>
            <div className="modal-footer">
              <button className="modal-button" onClick={() => {
                setAgreedToTerms(true);
                setShowTermsModal(false);
              }}>
                Accept and Continue
              </button>
              <button className="modal-button-secondary" onClick={() => setShowTermsModal(false)}>
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}