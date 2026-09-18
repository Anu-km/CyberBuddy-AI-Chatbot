import MessageBubble from "./MessageBubble";
import { useAutoScroll } from "../../shared/hooks/useAutoScroll";

type Props = {
  messages: { role: "user" | "bot"; text: string; time?: string }[];
  typing: boolean;
};

export default function ChatBox({ messages, typing }: Props) {
  const ref = useAutoScroll(messages);

  return (
    <div className="chat-container" ref={ref}>
      {messages.map((m, i) => (
        <MessageBubble
          key={i}
          role={m.role}
          text={m.text}
          time={m.time}
        />
      ))}

      {typing && (
        <div className="message bot">
          <div className="bubble typing">Analyzing…</div>
        </div>
      )}
    </div>
  );
}
