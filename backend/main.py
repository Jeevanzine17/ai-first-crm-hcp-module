from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from agent.tools import extract_interaction
from agent.graph import graph

from database import Base, engine
import models
import os

# Load environment variables
load_dotenv()

app = FastAPI()

# Create tables if not exist
Base.metadata.create_all(bind=engine)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------
# ROOT CHECK
# ---------------------------------------------------

@app.get("/")
def root():
    return {"status": "CRM AI Backend Running"}

# ---------------------------------------------------
# BASIC EXTRACTION (for debugging only)
# ---------------------------------------------------

@app.post("/agent/extract")
def extract(data: dict):
    if "text" not in data:
        return {"error": "Text field missing"}

    result = extract_interaction(data["text"])
    return {"extracted": result}

# ---------------------------------------------------
# LANGGRAPH AI AGENT (REAL AI-FIRST ENDPOINT)
# ---------------------------------------------------

@app.post("/agent/chat")
def chat(data: dict):
    if "text" not in data:
        return {"error": "Text field missing"}

    result = graph.invoke({
        "messages": [HumanMessage(content=data["text"])]
    })

    return {"response": result}