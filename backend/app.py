from flask import Flask, jsonify, request
from flask_cors import CORS
from .config import config
from .backboard_client import run_coroutine, ensure_thread, send_message

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    @app.post("/api/chat")
    def chat():
        data = request.get_json() or {}
        user_id = data.get("userId")
        message = data.get("message", "")
        # later: look up per-user thread in DB; for now, create a new one
        thread = run_coroutine(ensure_thread(config.BACKBOARD_ASSISTANT_ID))
        reply = run_coroutine(send_message(thread.thread_id, message))
        return jsonify({"reply": reply, "threadId": thread.thread_id})

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=config.DEBUG)
