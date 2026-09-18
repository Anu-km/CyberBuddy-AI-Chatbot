import { useState } from "react";

export type Role = "user" | "bot";
export type Message = { role: Role; text: string; time?: string };

export function useChatStore() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [typing, setTyping] = useState(false);

  return { messages, setMessages, typing, setTyping };
}
