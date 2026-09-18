export default function ChatBox({ messages, typing }: any) {
  return (
    <div className="terminal-body">
      {messages.map((m: any, i: number) => (
        <div key={i} className={`log ${m.role}`}>
          <span className="prompt">{m.role === "user" ? "user@kali:$" : "cyber@ai:$"}</span>
          <span className="text">{m.text}</span>
        </div>
      ))}

      {typing && (
        <div className="log bot">
          <span className="prompt">cyber@ai:$</span>
          <span className="text typing">processing...</span>
        </div>
      )}
    </div>
  );
}
