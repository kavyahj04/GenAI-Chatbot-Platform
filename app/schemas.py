"""
Request / Response schemas (Pydantic) for the FastAPI routes.
These are separate from the document models in models.py.
"""
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel


# ─────────────────────────────────────────────────────────────────────────────
# /session/start
# ─────────────────────────────────────────────────────────────────────────────
class SessionStartRequest(BaseModel):
    pid: str                                  # Prolific participant ID
    study_id: Optional[str] = None            # Prolific study ID
    prolific_session_id: Optional[str] = None # Prolific SESSION_ID param
    qr_pre: Optional[str] = None              # Qualtrics PreSurvey ResponseID
    experiment_id: str                        # MongoDB ObjectId string of experiment
    client_metadata: Optional[Dict[str, Any]] = None


class SessionStartResponse(BaseModel):
    chat_session_id: str
    condition_id: str
    condition_name: str


# ─────────────────────────────────────────────────────────────────────────────
# /session/end
# ─────────────────────────────────────────────────────────────────────────────
class SessionEndRequest(BaseModel):
    chat_session_id: str


class SessionEndResponse(BaseModel):
    redirect_url: str


# ─────────────────────────────────────────────────────────────────────────────
# /chat
# ─────────────────────────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    chat_session_id: str
    user_message: str
    client_turn_id: Optional[str] = None      # optional frontend idempotency key


class ChatResponse(BaseModel):
    assistant_message: str
    condition_id: str
    model: str
    usage: Optional[Dict[str, Any]] = None


# ─────────────────────────────────────────────────────────────────────────────
# /chat/final  (last turn — also ends the session and returns redirect)
# ─────────────────────────────────────────────────────────────────────────────
class FinalChatRequest(BaseModel):
    chat_session_id: str
    user_message: str


class FinalChatResponse(BaseModel):
    assistant_message: str
    redirect_url: str


# ─────────────────────────────────────────────────────────────────────────────
# /admin  export query params
# ─────────────────────────────────────────────────────────────────────────────
class ExportFormat(str):
    CSV = "csv"
    JSON = "json"
