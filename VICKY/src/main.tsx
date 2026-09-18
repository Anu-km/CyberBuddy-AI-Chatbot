// import React from "react";
// import ReactDOM from "react-dom/client";
// import App from "./App";
// // import "./index.css";
// import "./styles/theme.css";

// ReactDOM.createRoot(document.getElementById("root")!).render(
//   <React.StrictMode>
//     <App />
//   </React.StrictMode>
// );

import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./styles/theme.css"; // your global styles

// Create a session_id cookie if it doesn't exist
function setSessionCookie() {
  const existing = document.cookie
    .split("; ")
    .find(row => row.startsWith("session_id="));

  if (!existing) {
    const sessionId = crypto.randomUUID();
    document.cookie = `session_id=${sessionId}; path=/; SameSite=Lax`;
    console.log("Session cookie created:", sessionId);
  }
}

// Call it once on app load
setSessionCookie();

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
