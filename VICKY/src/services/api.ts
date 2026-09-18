const BACKEND_URL = "http://127.0.0.1:5001"; // change if your backend runs on another port

export async function sendMessage(message: string) {
  const res = await fetch(`${BACKEND_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || "Backend error");
  }

  return res.json(); // { reply: string }
}
