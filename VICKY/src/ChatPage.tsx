import { useState } from "react";
import ChatBox from "./components/ChatBox";
import Input from "./components/Input";

const uid = localStorage.getItem("uid") || crypto.randomUUID();
localStorage.setItem("uid", uid);

export default function ChatPage() {
  const [messages, setMessages] = useState<any[]>([]);
  const [typing, setTyping] = useState(false);

  const typeText = async (text: string) => {
    let current = "";
    for (let char of text) {
      current += char;
      setMessages(prev => {
        const copy = [...prev];
        copy[copy.length - 1].text = current;
        return copy;
      });
      await new Promise(r => setTimeout(r, 12));
    }
  };

  async function sendMessage(text: string) {
    if (!text.trim()) return;

    setMessages(prev => [...prev, { role: "user", text }]);
    setTyping(true);

    const res = await fetch(`${import.meta.env.VITE_API_URL}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user: uid, message: text })
    });

    const data = await res.json();
    setTyping(false);

    setMessages(prev => [...prev, { role: "bot", text: "" }]);
    await typeText(data.reply);
  }

//   return (
//     <div className="chat-panel-bg">
//       <div className="chat-panel-glass">
//         <div className="chat-header">🛡 CyberBuddy</div>
//         <ChatBox messages={messages} typing={typing} />
//         <Input onSend={sendMessage} />
//       </div>
//     </div>
//   );
// }
// ❌ REMOVE anything like this:
// <div className="terminal-header">...</div>
// <div className="terminal-input">...</div>
// user@kali:$ prompt

// ✅ Keep only this structure:
return (
  <div className="glass-card">
    <div className="glass-header">Ai Chatbot</div>
    <ChatBox messages={messages} typing={typing} />
    <Input onSend={sendMessage} />
  </div>
);
}
