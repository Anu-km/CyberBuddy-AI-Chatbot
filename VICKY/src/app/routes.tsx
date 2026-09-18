
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ChatPage from "../features/chat/ChatPage";

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ChatPage />} />
      </Routes>
    </BrowserRouter>
  );
}
