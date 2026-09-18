# 🛡️ CyberBuddy AI Chatbot

**CyberBuddy AI Chatbot** is a cybersecurity-focused AI assistant developed to help users learn cybersecurity, ask security-related questions, and explore security analysis tools through an interactive chat interface.

The project contains a **React + TypeScript frontend** and a **Python backend** with cybersecurity-focused modules.

---

## ✨ Features

* 🤖 AI-powered cybersecurity chatbot
* 💬 Interactive chat interface
* 🧠 Conversation memory
* 🔐 Cybersecurity-focused responses
* 🛡️ Security analysis modules
* 🔎 Cybersecurity utility tools
* 🚨 Threat/security monitoring components
* 🌐 React-based web interface
* 🐍 Python backend
* 🔌 API-based frontend/backend communication

---

## 🏗️ Project Structure

```text
CyberBuddy-AI-Chatbot/
│
├── VICKY/                         # Frontend
│   ├── public/
│   ├── src/
│   │   ├── app/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── features/
│   │   │   ├── chat/
│   │   │   └── security/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── shared/
│   │   ├── App.tsx
│   │   ├── ChatPage.tsx
│   │   ├── index.css
│   │   └── main.tsx
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── khs/                           # Python Backend
│   ├── app.py
│   ├── audit.py
│   ├── auth.py
│   ├── chat.py
│   ├── check_apis.py
│   ├── cybertools.py
│   ├── db.py
│   ├── files.py
│   ├── knowledge.py
│   ├── memory.py
│   ├── models.py
│   ├── security.py
│   ├── security_engine.py
│   ├── sockets.py
│   ├── urlhaus_checker.py
│   ├── vision.py
│   └── requirements.txt
│
├── package.json
├── package-lock.json
└── .gitignore
```

---

## 🛠️ Technologies

### Frontend

* React
* TypeScript
* Vite
* HTML5
* CSS3

### Backend

* Python
* Flask
* REST APIs

### Security

* Cybersecurity analysis
* Security engine
* URL security checking
* Threat analysis components
* Cybersecurity utilities

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Anu-km/CyberBuddy-AI-Chatbot.git
cd CyberBuddy-AI-Chatbot
```

---

### 2. Frontend Setup

```bash
cd VICKY
npm install
npm run dev
```

The frontend will be available at:

```text
http://localhost:5173
```

---

### 3. Backend Setup

Open another terminal and navigate to the backend:

```bash
cd khs
```

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Start the backend:

```bash
python app.py
```

---

## 🔐 Environment Variables

If the application requires API keys or other sensitive configuration, create a `.env` file locally.

Example:

```env
API_KEY=your_api_key_here
```

**Do not upload real API keys, passwords, tokens, or other secrets to GitHub.**

---

## 🎯 Project Objective

The objective of CyberBuddy is to develop an AI-based cybersecurity assistant that can support:

* Cybersecurity learning
* Security-related questions
* Cybersecurity analysis
* Security tool assistance
* Threat-related information
* Interactive cybersecurity education

---

## 🔮 Future Scope

Possible future improvements include:

* Advanced RAG-based cybersecurity knowledge
* Integration with additional threat-intelligence sources
* Real-time threat detection
* Improved AI memory
* Advanced security automation
* User authentication
* Cloud deployment
* Security dashboard improvements

---

## 👨‍💻 Author

**Vicky Kumar**

B.Tech — Computer Science & Engineering
Cybersecurity Domain

---

## ⚠️ Disclaimer

CyberBuddy is intended for **educational, research, and authorized cybersecurity purposes only**.

Only perform security testing or security analysis on systems, applications, and networks for which you have proper authorization.

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.
