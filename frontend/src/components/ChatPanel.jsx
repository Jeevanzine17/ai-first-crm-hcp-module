import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { setFormData } from "../features/chatSlice";

const ChatPanel = () => {
  const [message, setMessage] = useState("");
  const [chatResponse, setChatResponse] = useState(null);
  const dispatch = useDispatch();

  const handleSend = async () => {
    if (!message.trim()) return;

    const res = await fetch("http://127.0.0.1:8000/agent/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: message }),
    });

    const data = await res.json();
    const result = data.response?.result;

    // --------------------------------------------------
    // 1️ If Log Interaction Tool
    // --------------------------------------------------
    if (result?.status === "logged") {
      dispatch(setFormData(result.data));
    }

    // --------------------------------------------------
    // 2️ If Follow-up Suggestion Tool
    // --------------------------------------------------
    if (result?.suggestion) {
      dispatch(
        setFormData({
          follow_up: result.suggestion,
        })
      );
    }

    // --------------------------------------------------
    // 3️ If Compliance Tool
    // --------------------------------------------------
    if (result?.compliance_flag !== undefined) {
      setChatResponse(
        result.compliance_flag
          ? `⚠️ Compliance Alert: ${result.reason}`
          : "✅ No compliance risks detected."
      );
    }

    // --------------------------------------------------
    // 4️ If Insight Tool
    // --------------------------------------------------
    if (result?.hcp_name) {
      setChatResponse(
        `📊 ${result.hcp_name} has ${result.total_interactions} interactions.\nSentiment history: ${result.sentiment_history.join(", ")}`
      );
    }

    // --------------------------------------------------
    // 5️ If Edit Tool
    // --------------------------------------------------
    if (result?.status === "updated") {
      setChatResponse("✅ Interaction updated successfully.");
    }

    setMessage("");
  };

  return (
    <>
      <h3>🤖 AI Assistant</h3>
      <p style={{ fontSize: 13, color: "#6b7280" }}>
        Log interaction details here via chat
      </p>

      <div
        style={{
          background: "#e0f2fe",
          padding: 14,
          borderRadius: 10,
          marginTop: 20,
        }}
      >
        Log interaction details here (e.g., “Met Dr. Smith, discussed Product-X efficacy...”)
      </div>

      <div style={{ marginTop: 20 }}>
        <textarea
          rows="3"
          placeholder="Describe interaction..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          style={{ width: "100%", padding: 10 }}
        />

        <button
          onClick={handleSend}
          style={{
            marginTop: 10,
            background: "#2563eb",
            color: "white",
            padding: "10px 20px",
            borderRadius: 10,
            border: "none",
          }}
        >
          Send
        </button>
      </div>

      {chatResponse && (
        <div
          style={{
            marginTop: 20,
            background: "#f3f4f6",
            padding: 10,
            borderRadius: 10,
            whiteSpace: "pre-wrap",
          }}
        >
          {chatResponse}
        </div>
      )}
    </>
  );
};

export default ChatPanel;