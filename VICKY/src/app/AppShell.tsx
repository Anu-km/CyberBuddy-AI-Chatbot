import React from "react";
import "../styles/theme.css";

export default function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="app-bg">
      <div className="app-overlay" />
      <main className="app-container">{children}</main>
    </div>
  );
}
