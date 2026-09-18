import { useState } from "react";

export default function Input({ onSend }: { onSend: (text: string) => void }) {
  const [text, setText] = useState("");

  const handleSend = () => {
    if (!text.trim()) return;
    onSend(text);
    setText("");
  };

  return (
    <div className="terminal-input">
      <span className="prompt">user@kali:$</span>
      <input
        value={text}
        onChange={e => setText(e.target.value)}
        onKeyDown={e => e.key === "Enter" && handleSend()}
        placeholder="type command..."
      />
      <button onClick={handleSend}>↵</button>
    </div>
  );
}
