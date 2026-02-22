# AI‑First CRM – HCP Interaction Module

## Overview

AI‑First CRM is a healthcare‑focused Customer Relationship Management (CRM) system designed specifically for Life Sciences field representatives.
This module demonstrates an **AI‑driven HCP (Healthcare Professional) interaction logging system** powered by:

* **Frontend:** React + Redux
* **Backend:** FastAPI (Python)
* **AI Agent Framework:** LangGraph
* **LLM Provider:** Groq (LLaMA models)
* **Database:** SQL (MySQL/PostgreSQL compatible via SQLAlchemy)
* **Font:** Google Inter

The system enables representatives to log HCP interactions either via:

1. Structured form input
2. Conversational AI interface

The AI agent extracts structured data from natural language and logs it into the CRM database.

---

# Architecture

## Frontend (React + Redux)

* Chat‑based interaction panel
* Structured Log Interaction form
* AI‑driven extraction
* Redux state management
* Enterprise‑style UI layout

## Backend (FastAPI)

* REST APIs
* LangGraph AI orchestration
* Groq LLM integration
* SQLAlchemy ORM
* Strict Pydantic validation

## AI Agent (LangGraph)

LangGraph orchestrates tool usage based on user intent.
The agent routes user inputs to appropriate tools.

---

# LangGraph Tools (5 Required Tools)

## 1️⃣ Log Interaction Tool

Purpose:

* Accepts natural language interaction text
* Uses LLM for entity extraction
* Validates structured schema
* Saves interaction into database

Key Fields Extracted:

* HCP Name
* Interaction Type
* Date & Time
* Topics Discussed
* Materials Shared
* Samples Distributed
* Sentiment
* Outcomes
* Follow‑Up

---

## 2️⃣ Edit Interaction Tool

Purpose:

* Modify specific fields of an existing interaction
* Uses interaction ID
* Updates database record

---

## 3️⃣ HCP Insight Tool

Purpose:

* Retrieve historical summary of an HCP
* Total interactions
* Sentiment trend

---

## 4️⃣ Compliance Check Tool

Purpose:

* Detect compliance risks (e.g., off‑label discussions)
* Flags potential regulatory violations

---

## 5️⃣ Follow‑Up Recommendation Tool

Purpose:

* Suggest next best action based on sentiment
* Supports AI‑guided engagement strategy

---

# Installation Guide

## 1. Clone Repository

```
git clone <repository-url>
cd ai-first-crm-hcp-module
```

---

## 2. Backend Setup

```
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` file inside backend folder:

```

```

Run backend:

```
uvicorn main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

Swagger docs:

```
http://127.0.0.1:8000/docs
```

---

## 3. Frontend Setup

```
cd frontend
npm install
npm start
```

Frontend runs at:

```
http://localhost:3000
```

---

# API Endpoints

## POST /agent/extract

Extract structured interaction data using AI.

## POST /agent/chat

LangGraph‑powered agent routing for tool execution.

---

# Database Schema

Core Tables:

* Interaction
* Material
* Sample

Each interaction stores related materials and samples via foreign keys.

---

# Enterprise Design Principles Applied

* Strict schema validation
* Deterministic LLM extraction (temperature=0)
* Error handling & validation safeguards
* Modular tool architecture
* Clear separation of concerns
* Production‑oriented folder structure

---

# Demonstration Flow (For Video Submission)

1. Log interaction via chat
2. Show structured extraction auto‑populating form
3. Demonstrate Edit Interaction
4. Demonstrate HCP Insights
5. Demonstrate Compliance Check
6. Demonstrate Follow‑Up Recommendation
7. Explain LangGraph routing logic
8. Explain backend architecture

---

# What I Learned from Task 1

* Designing AI‑first workflows requires structured schema enforcement
* LangGraph provides deterministic orchestration for tool‑based AI agents
* Strict validation is critical when integrating LLMs in enterprise systems
* AI can significantly improve field rep productivity in healthcare CRM systems

---

# Future Improvements

* Authentication & role‑based access
* Audit logging for compliance
* Production database migration (PostgreSQL)
* Docker deployment
* CI/CD pipeline
* LLM response caching

---

# Security Notice

* API keys are never committed to repository
* `.env` is ignored via `.gitignore`
* Secrets must be stored securely in production

---

# Conclusion

This project demonstrates a functional AI‑first CRM HCP interaction module with:

* Working LangGraph agent
* 5 enterprise‑oriented tools
* Groq LLM integration
* Full stack implementation

Designed with scalability and production readiness in mind.
