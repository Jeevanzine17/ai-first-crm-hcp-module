import React from "react";
import { useSelector } from "react-redux";

const FormPanel = () => {
  const data = useSelector((state) => state.chat.formData);

  return (
    <div style={{ height: "90vh", overflowY: "auto" }}>

      <h2 style={{ fontWeight: 600 }}>Log HCP Interaction</h2>

      <div style={{
        background: "#f8fafc",
        padding: 16,
        borderRadius: 8,
        marginTop: 20
      }}>
        <h4>Interaction Details</h4>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
          <div>
            <label>HCP Name</label>
            <input placeholder="Search or select HCP..." value={data?.hcp_name || ""} readOnly />
          </div>

          <div>
            <label>Interaction Type</label>
            <select value={data?.interaction_type || ""} disabled>
              <option>Meeting</option>
              <option>Call</option>
              <option>Email</option>
            </select>
          </div>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginTop: 16 }}>
          <div>
            <label>Date</label>
            <input value={data?.date || ""} readOnly />
          </div>

          <div>
            <label>Time</label>
            <input value={data?.time || ""} readOnly />
          </div>
        </div>

        <div style={{ marginTop: 16 }}>
          <label>Attendees</label>
          <input placeholder="Enter names or search..." value={data?.attendees?.join(", ") || ""} readOnly />
        </div>

        <div style={{ marginTop: 16 }}>
          <label>Topics Discussed</label>
          <textarea rows="3" value={data?.topics_discussed?.join(", ") || ""} readOnly />
        </div>

        <div style={{ marginTop: 10, fontSize: 13, color: "#3b82f6" }}>
          🎙 Summarize from Voice Note (Requires Consent)
        </div>
      </div>

      {/* Materials Section */}
      <div style={{ marginTop: 20 }}>
        <h4>Materials Shared / Samples Distributed</h4>

        <div style={{ border: "1px solid #e5e7eb", padding: 12, borderRadius: 8 }}>
          <div style={{ display: "flex", justifyContent: "space-between" }}>
            <strong>Materials Shared</strong>
            <button style={{ fontSize: 12 }}>🔍 Search/Add</button>
          </div>
          {data?.materials_shared?.length > 0
            ? data.materials_shared.map((m, i) => (
                <div key={i}>{m.name}</div>
              ))
            : <div style={{ color: "#9ca3af" }}>No materials added.</div>}
        </div>

        <div style={{ border: "1px solid #e5e7eb", padding: 12, borderRadius: 8, marginTop: 12 }}>
          <div style={{ display: "flex", justifyContent: "space-between" }}>
            <strong>Samples Distributed</strong>
            <button style={{ fontSize: 12 }}>+ Add Sample</button>
          </div>
          {data?.samples_distributed?.length > 0
            ? data.samples_distributed.map((s, i) => (
                <div key={i}>{s.product_name} – {s.quantity}</div>
              ))
            : <div style={{ color: "#9ca3af" }}>No samples added.</div>}
        </div>
      </div>

      {/* Sentiment */}
      <div style={{ marginTop: 20 }}>
        <h4>Observed/Inferred HCP Sentiment</h4>
        <div style={{ display: "flex", gap: 30 }}>
          <label><input type="radio" checked={data?.sentiment==="positive"} readOnly/> 😊 Positive</label>
          <label><input type="radio" checked={data?.sentiment==="neutral"} readOnly/> 😐 Neutral</label>
          <label><input type="radio" checked={data?.sentiment==="negative"} readOnly/> 😟 Negative</label>
        </div>
      </div>

      <div style={{ marginTop: 20 }}>
        <h4>Outcomes</h4>
        <textarea rows="2" value={data?.outcomes || ""} readOnly />
      </div>

      <div style={{ marginTop: 20 }}>
        <h4>Follow-up Actions</h4>
        <textarea rows="2" value={data?.follow_up || ""} readOnly />
      </div>
    </div>
  );
};

export default FormPanel;