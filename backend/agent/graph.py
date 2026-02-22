from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
import os
import re

from agent.tools import (
    log_interaction_tool,
    edit_interaction_tool,
    hcp_insight_tool,
    compliance_check_tool,
    followup_recommendation_tool
)

# ---------------------------------------------------
# LLM MODEL
# ---------------------------------------------------

model = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

builder = StateGraph(dict)

# ---------------------------------------------------
# ROUTER NODE
# ---------------------------------------------------

def agent_node(state):
    user_input_raw = state["messages"][-1].content
    user_input = user_input_raw.lower()

    # ---------------------------------------------------
    # 1️ LOG INTERACTION
    # ---------------------------------------------------
    if "log interaction" in user_input:
        return {
            "result": log_interaction_tool.invoke({
                "text": user_input_raw
            })
        }

    # ---------------------------------------------------
    # 2️ EDIT INTERACTION (Dynamic UUID parsing)
    # ---------------------------------------------------
    elif "edit interaction" in user_input:

        # Extract UUID
        match = re.search(r"[a-f0-9\-]{36}", user_input)

        if not match:
            return {"result": {"error": "No valid interaction ID found"}}

        interaction_id = match.group(0)

        # Extract sentiment change if mentioned
        if "neutral" in user_input:
            value = "neutral"
        elif "positive" in user_input:
            value = "positive"
        elif "negative" in user_input:
            value = "negative"
        else:
            value = "neutral"

        return {
            "result": edit_interaction_tool.invoke({
                "interaction_id": interaction_id,
                "field": "sentiment",
                "value": value
            })
        }

    # ---------------------------------------------------
    # 3️ HCP INSIGHT (Dynamic name parsing)
    # ---------------------------------------------------
    elif "insight" in user_input or "show insights" in user_input:

        # Extract name after "for"
        match = re.search(r"for (.+)", user_input_raw, re.IGNORECASE)

        if not match:
            return {"result": {"error": "No HCP name provided"}}

        hcp_name = match.group(1).strip()

        return {
            "result": hcp_insight_tool.invoke({
                "hcp_name": hcp_name
            })
        }

    # ---------------------------------------------------
    # 4️ COMPLIANCE CHECK
    # ---------------------------------------------------
    elif "off-label" in user_input:
        return {
            "result": compliance_check_tool.invoke({
                "text": user_input_raw
            })
        }

    # ---------------------------------------------------
    # 5️ FOLLOW-UP RECOMMENDATION
    # ---------------------------------------------------
    elif "recommend" in user_input or "next action" in user_input:

        if "positive" in user_input:
            sentiment = "positive"
        elif "neutral" in user_input:
            sentiment = "neutral"
        elif "negative" in user_input:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return {
            "result": followup_recommendation_tool.invoke({
                "sentiment": sentiment
            })
        }

    # ---------------------------------------------------
    # 6️ FALLBACK --> LLM RESPONSE
    # ---------------------------------------------------
    else:
        response = model.invoke(state["messages"])
        return {"result": response.content}


# ---------------------------------------------------
# BUILD GRAPH
# ---------------------------------------------------

builder.add_node("agent", agent_node)
builder.set_entry_point("agent")
builder.add_edge("agent", END)

graph = builder.compile()