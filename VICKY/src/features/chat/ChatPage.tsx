import { useState } from "react";
import ChatBox from "./ChatBox";
import { useChatStore } from "./chat.store";
import { sendChat } from "./chat.service";
import Input from "../../shared/ui/Input";

const uid = localStorage.getItem("uid") || crypto.randomUUID();
localStorage.setItem("uid", uid);

export default function ChatPage() {
  const { messages, setMessages, typing, setTyping } = useChatStore();

  const typeText = async (text: string) => {
    let current = "";
    for (const ch of text) {
      current += ch;
      setMessages(prev => {
        const copy = [...prev];
        copy[copy.length - 1].text = current;
        return copy;
      });
      await new Promise(r => setTimeout(r, 15));
    }
  };

  async function onSend(text: string) {
    if (!text.trim()) return;

    setMessages(prev => [...prev, { role: "user", text }]);
    setTyping(true);

    try {
      const data = await sendChat(uid, text);
      setTyping(false);

      setMessages(prev => [...prev, { role: "bot", text: "" }]);
      await typeText(data.reply);
    } catch (e) {
      setTyping(false);
      setMessages(prev => [
        ...prev,
        { role: "bot", text: "Server error. Try again." }
      ]);
    }
  }

  return (
    <div className="glass-card">
      <div
        className="glass-header"
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center"
        }}
      >
        <span>AI CHATBOT</span>
      </div>

      <ChatBox messages={messages} typing={typing} />

      <Input onSend={onSend} />
    </div>
  );
}