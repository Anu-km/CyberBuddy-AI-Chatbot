export async function sendChat(user: string, message: string) {
  const res = await fetch(`${import.meta.env.VITE_API_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user, message }),
  });

  if (!res.ok) {
    throw new Error("Failed to send message to API");
  }

  return res.json(); // expected { reply: string }
}
