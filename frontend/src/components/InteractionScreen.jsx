import React from "react";
import FormPanel from "./FormPanel";
import ChatPanel from "./ChatPanel";
import "../index.css";

const InteractionScreen = () => {
  return (
    <div className="page-wrapper">
      <div className="left-container card">
        <FormPanel />
      </div>

      <div className="right-container card">
        <ChatPanel />
      </div>
    </div>
  );
};

export default InteractionScreen;