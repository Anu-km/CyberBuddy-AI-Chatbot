import { useState } from "react";

export default function ScanWidget() {
  const [status, setStatus] = useState("Idle");

  function startScan() {
    setStatus("Scanning network…");
    setTimeout(() => setStatus("Scan complete. No critical issues found."), 2500);
  }

  return (
    <div className="panel">
      <h3>Network Scan</h3>
      <p>Status: {status}</p>
      <button onClick={startScan}>Start Scan</button>
    </div>
  );
}
