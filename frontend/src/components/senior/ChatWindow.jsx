import React, { useState, useRef, useEffect } from "react";

function ChatWindow({ seniorId, role }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    // Add user message to UI
    const userMsg = { role: "user", content: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          userId: seniorId,
          message: input,
          role: role,
        }),
      });

      const data = await response.json();
      
      if (response.ok) {
        const assistantMsg = { role: "assistant", content: data.reply };
        setMessages((prev) => [...prev, assistantMsg]);
      } else {
        const errorMsg = { role: "assistant", content: "Sorry, I had trouble understanding. Please try again." };
        setMessages((prev) => [...prev, errorMsg]);
      }
    } catch (error) {
      console.error("Chat error:", error);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Connection error. Please try again." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-window">
      <div className="chat-header">
        <h2>💬 Talk to Your Assistant</h2>
        <p>Ask about your medications, appointments, or health information</p>
      </div>

      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="chat-empty">
            <p>👋 Hello! I'm here to help you with your health reminders.</p>
            <p>You can ask me:</p>
            <ul>
              <li>"What medicine do I take this morning?"</li>
              <li>"When is my next doctor visit?"</li>
              <li>"What does my blood test mean?"</li>
            </ul>
          </div>
        )}

        {messages.map((msg, idx) => (
          <div key={idx} className={`chat-message chat-${msg.role}`}>
            <div className="message-bubble">
              {msg.content}
            </div>
          </div>
        ))}

        {loading && (
          <div className="chat-message chat-assistant">
            <div className="message-bubble">
              <span className="typing-indicator">●●●</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && handleSend()}
          placeholder="Type your question..."
          className="chat-input"
          style={{ fontSize: "16px" }}
        />
        <button
          onClick={handleSend}
          disabled={loading || !input.trim()}
          className="chat-send-btn"
          style={{ fontSize: "16px", padding: "12px 24px" }}
        >
          {loading ? "Sending..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default ChatWindow;
