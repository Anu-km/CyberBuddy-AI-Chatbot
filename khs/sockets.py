from flask_socketio import SocketIO

# Windows-safe async mode
socketio = SocketIO(cors_allowed_origins="*", async_mode="threading")

# Example socket events (optional)
@socketio.on("connect")
def handle_connect():
    print("Client connected")

@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")
