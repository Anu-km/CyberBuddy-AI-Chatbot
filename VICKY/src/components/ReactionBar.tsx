export default function ReactionBar({ onReact }: any) {
  return (
    <div className="reactions">
      {["👍", "👎", "❤️"].map(r => (
        <span key={r} onClick={() => onReact(r)}>{r}</span>
      ))}
    </div>
  );
}
