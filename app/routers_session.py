from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from .db import get_db
from . import schemas, services

router = APIRouter(prefix="/session", tags=["session"])


@router.post("/start", response_model=schemas.SessionStartResponse)
async def start_session(
    payload: schemas.SessionStartRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    """
    Creates or retrieves a participant, assigns A/B condition (stable per PID),
    opens a new ChatSession, and returns the chat_session_id.
    """
    participant = await services.get_or_create_participant(
        db=db,
        pid=payload.pid,
        study_id=payload.study_id,
    )

    try:
        chat_session, condition = await services.create_chat_session(
            db=db,
            participant=participant,
            experiment_id=payload.experiment_id,
            qr_pre=payload.qr_pre,
            prolific_session_id=payload.prolific_session_id,
            client_metadata=payload.client_metadata,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    await services.log_event(
        db=db,
        event_type="session_start",
        description=f"Session started for pid={payload.pid}",
        chat_session_id=chat_session["id"],
        participant_id=participant["id"],
    )

    return schemas.SessionStartResponse(
        chat_session_id=chat_session["id"],
        condition_id=condition["id"],
        condition_name=condition["name"],
    )


@router.post("/end", response_model=schemas.SessionEndResponse)
async def end_session(
    payload: schemas.SessionEndRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    """
    Marks the session as completed and returns the Qualtrics post-survey redirect URL.
    """
    try:
        session = await services.end_chat_session(db=db, chat_session_id=payload.chat_session_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    condition = await services.get_condition(db, session["condition_id"])

    # Look up participant pid for the redirect URL
    participant_doc = await db.participants.find_one({"_id": ObjectId(session["participant_id"])})
    pid = participant_doc["pid"] if participant_doc else ""

    redirect_url = services.build_qualtrics_redirect(
        session=session, condition=condition, pid=pid
    )

    await services.log_event(
        db=db,
        event_type="session_end",
        description=f"Session ended for pid={pid}",
        chat_session_id=session["id"],
        participant_id=session["participant_id"],
    )

    return schemas.SessionEndResponse(redirect_url=redirect_url)
