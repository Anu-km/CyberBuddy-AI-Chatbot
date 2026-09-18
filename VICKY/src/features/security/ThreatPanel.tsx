export default function ThreatPanel() {
  return (
    <div className="panel">
      <h3>Threat Intelligence</h3>
      <ul>
        <li>🔴 High Risk: 2 active threats</li>
        <li>🟠 Medium Risk: 5 alerts</li>
        <li>🟢 Low Risk: System stable</li>
      </ul>
    </div>
  );
}
