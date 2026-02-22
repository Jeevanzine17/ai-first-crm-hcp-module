from groq import Groq
import os
import json
import uuid
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError, Field
from typing import List, Optional
from langchain_core.tools import tool
from sqlalchemy.exc import SQLAlchemyError

from database import SessionLocal
from models import Interaction, Material, Sample

# --------------------------------------------------
# ENVIRONMENT SETUP
# --------------------------------------------------

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables")

client = Groq(api_key=GROQ_API_KEY)

# --------------------------------------------------
# STRICT SCHEMA DEFINITIONS
# --------------------------------------------------

class MaterialSchema(BaseModel):
    name: str
    type: str


class SampleSchema(BaseModel):
    product_name: str
    quantity: int


class InteractionSchema(BaseModel):
    hcp_name: Optional[str]
    interaction_type: Optional[str]
    date: Optional[str]
    time: Optional[str]

    attendees: List[str] = Field(default_factory=list)
    topics_discussed: List[str] = Field(default_factory=list)
    materials_shared: List[MaterialSchema] = Field(default_factory=list)
    samples_distributed: List[SampleSchema] = Field(default_factory=list)

    sentiment: Optional[str]
    outcomes: Optional[str]
    follow_up: Optional[str]


# --------------------------------------------------
# EXTRACTION ENGINE
# --------------------------------------------------

def extract_interaction(text: str):

    system_prompt = """
You are a pharmaceutical CRM extraction engine.

Return STRICT VALID JSON only.

Rules:
- No markdown
- No explanations
- Always return valid JSON
- Arrays must always be arrays
- Sentiment must be: positive, neutral, or negative
- If unknown, use null
"""

    schema_template = {
        "hcp_name": None,
        "interaction_type": None,
        "date": None,
        "time": None,
        "attendees": [],
        "topics_discussed": [],
        "materials_shared": [],
        "samples_distributed": [],
        "sentiment": None,
        "outcomes": None,
        "follow_up": None
    }

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            temperature=0,
            max_tokens=500,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Extract CRM interaction data from this:\n\n{text}\n\nReturn this exact JSON schema:\n{json.dumps(schema_template)}"
                }
            ]
        )

        raw = response.choices[0].message.content.strip()
        parsed = json.loads(raw)

        # ======================================================
        # DEFENSIVE NORMALIZATION (Production Safe)
        # ======================================================

        # ---- Materials ----
        materials = parsed.get("materials_shared")
        if not isinstance(materials, list):
            materials = []

        normalized_materials = []
        for m in materials:
            if isinstance(m, str):
                normalized_materials.append({
                    "name": m,
                    "type": "other"
                })
            elif isinstance(m, dict):
                normalized_materials.append(m)

        parsed["materials_shared"] = normalized_materials

        # ---- Samples ----
        samples = parsed.get("samples_distributed")

        if isinstance(samples, int):
            samples = [{
                "product_name": "Unknown Product",
                "quantity": samples
            }]
        elif not isinstance(samples, list):
            samples = []

        normalized_samples = []
        for s in samples:
            if isinstance(s, int):
                normalized_samples.append({
                    "product_name": "Unknown Product",
                    "quantity": s
                })
            elif isinstance(s, dict):
                normalized_samples.append(s)

        parsed["samples_distributed"] = normalized_samples

        # ---- Outcomes ----
        outcomes = parsed.get("outcomes")
        if isinstance(outcomes, list):
            parsed["outcomes"] = ", ".join(outcomes)
        elif not isinstance(outcomes, str):
            parsed["outcomes"] = None

        # ---- Follow Up ----
        follow = parsed.get("follow_up")
        if isinstance(follow, list):
            parsed["follow_up"] = ", ".join(follow)
        elif not isinstance(follow, str):
            parsed["follow_up"] = None

        # ---- Attendees Safe Check ----
        if not isinstance(parsed.get("attendees"), list):
            parsed["attendees"] = []

        # ---- Topics Safe Check ----
        if not isinstance(parsed.get("topics_discussed"), list):
            parsed["topics_discussed"] = []

        validated = InteractionSchema(**parsed)
        return validated.model_dump()

    except (json.JSONDecodeError, ValidationError) as e:
        print("Extraction validation error:", e)
        return {"error": "Validation failed"}

    except Exception as e:
        print("Extraction runtime error:", e)
        return {"error": str(e)}


# ==========================================================
# ===================== LANGGRAPH TOOLS ====================
# ==========================================================

# --------------------------------------------------
# 1️⃣ LOG INTERACTION TOOL
# --------------------------------------------------

@tool
def log_interaction_tool(text: str):
    """Logs a CRM interaction from natural language input."""

    data = extract_interaction(text)

    if "error" in data:
        return data

    db = SessionLocal()

    try:
        interaction = Interaction(
            id=str(uuid.uuid4()),
            hcp_name=data.get("hcp_name"),
            interaction_type=data.get("interaction_type"),
            date=data.get("date"),
            time=data.get("time"),
            sentiment=data.get("sentiment"),
            outcomes=data.get("outcomes"),
            follow_up=data.get("follow_up")
        )

        db.add(interaction)
        db.commit()

        for m in data.get("materials_shared", []):
            db.add(Material(
                id=str(uuid.uuid4()),
                interaction_id=interaction.id,
                name=m["name"],
                type=m["type"]
            ))

        for s in data.get("samples_distributed", []):
            db.add(Sample(
                id=str(uuid.uuid4()),
                interaction_id=interaction.id,
                product_name=s["product_name"],
                quantity=s["quantity"]
            ))

        db.commit()

        return {
            "status": "logged",
            "interaction_id": interaction.id,
            "data": data
        }

    except SQLAlchemyError as e:
        db.rollback()
        print("Database error:", e)
        return {"error": "Database error"}

    finally:
        db.close()


# --------------------------------------------------
# 2️  INTERACTION TOOL
# --------------------------------------------------

@tool
def edit_interaction_tool(interaction_id: str, field: str, value: str):
    """Edits a specific field of an existing interaction."""

    db = SessionLocal()

    try:
        interaction = db.query(Interaction).filter_by(id=interaction_id).first()

        if not interaction:
            return {"error": "Interaction not found"}

        if not hasattr(interaction, field):
            return {"error": "Invalid field name"}

        setattr(interaction, field, value)
        db.commit()

        return {"status": "updated", "interaction_id": interaction_id}

    except Exception as e:
        db.rollback()
        return {"error": str(e)}

    finally:
        db.close()


# --------------------------------------------------
# 3️ HCP INSIGHT TOOL
# --------------------------------------------------

@tool
def hcp_insight_tool(hcp_name: str):
    """Returns summary insights about an HCP."""

    db = SessionLocal()

    try:
        records = db.query(Interaction).filter_by(hcp_name=hcp_name).all()
        sentiments = [r.sentiment for r in records if r.sentiment]

        return {
            "hcp_name": hcp_name,
            "total_interactions": len(records),
            "sentiment_history": sentiments
        }

    finally:
        db.close()


# --------------------------------------------------
# 4️ COMPLIANCE CHECK TOOL
# --------------------------------------------------

@tool
def compliance_check_tool(text: str):
    """Flags compliance risks (e.g., off-label mentions)."""

    if "off-label" in text.lower():
        return {
            "compliance_flag": True,
            "reason": "Off-label discussion detected"
        }

    return {"compliance_flag": False}


# --------------------------------------------------
# 5️ FOLLOW-UP RECOMMENDATION TOOL
# --------------------------------------------------

@tool
def followup_recommendation_tool(sentiment: str):
    """Suggests next best action based on sentiment."""

    sentiment = (sentiment or "").lower()

    if sentiment == "positive":
        return {"suggestion": "Schedule follow-up meeting in 2 weeks"}
    elif sentiment == "neutral":
        return {"suggestion": "Share updated clinical data"}
    else:
        return {"suggestion": "Re-engage with value-based discussion"}