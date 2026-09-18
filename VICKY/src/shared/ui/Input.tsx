import { useState } from "react";

type InputProps = {
  onSend: (text: string) => void;
};

export default function Input({ onSend }: InputProps) {
  const [text, setText] = useState("");

  const handleSend = () => {
    if (!text.trim()) return;
    onSend(text.trim());
    setText(""); // clear input
  };

  return (
    <div className="input-box">
      <input
        value={text}
        onChange={e => setText(e.target.value)}
        onKeyDown={e => {
          if (e.key === "Enter") {
            e.preventDefault();
            handleSend();
          }
        }}
        placeholder="Ask CyberBuddy..."
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}
