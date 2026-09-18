
// import { formatTime } from "../../shared/utils/formatTime";

// type Props = {
//   role: "user" | "bot";
//   text: string;
//   time?: string;
// };

// export default function MessageBubble({ role, text, time }: Props) {
//   // Remove markdown ** from bot replies only
//   const cleanText =
//     role === "bot" ? text.replace(/\*\*/g, "") : text;

//   return (
//     <div className={`message ${role}`}>
//       <div className="bubble">
//         <div className="text">{cleanText}</div>
//         <div className="time">{time || formatTime(new Date())}</div>
//       </div>
//     </div>
//   );
// }
import { marked } from "marked";
import { formatTime } from "../../shared/utils/formatTime";

type Props = {
  role: "user" | "bot";
  text: string;
  time?: string;
};

export default function MessageBubble({ role, text, time }: Props) {
  return (
    <div className={`message ${role}`}>
      <div className="bubble">
        {role === "bot" ? (
          <div
            className="markdown"
            dangerouslySetInnerHTML={{ __html: marked.parse(text) }}
          />
        ) : (
          <div className="text">{text}</div>
        )}
        <div className="time">{time || formatTime(new Date())}</div>
      </div>
    </div>
  );
}
