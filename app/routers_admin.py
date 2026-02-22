import csv
import io
from typing import Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Response
from motor.motor_asyncio import AsyncIOMotorDatabase

from .db import get_db

router = APIRouter(prefix="/admin", tags=["admin"])

VALID_TABLES = {"participants", "sessions", "messages"}


@router.get("/sessions")
async def list_sessions(
    experiment_id: Optional[str] = None,
    condition_id: Optional[str] = None,
    status: Optional[str] = None,
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    """List chat sessions, optionally filtered by experiment, condition, or status."""
    query: dict = {}
    if experiment_id:
        query["experiment_id"] = experiment_id
    if condition_id:
        query["condition_id"] = condition_id
    if status:
        query["status"] = status

    cursor = db.chat_sessions.find(query).sort("started_at", -1).limit(500)
    docs = await cursor.to_list(length=500)
    for d in docs:
        d["id"] = str(d.pop("_id"))
    return docs


@router.get("/export")
async def export_data(
    experiment_id: Optional[str] = None,
    table: str = "messages",
    format: str = "csv",
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    """
    Export participants, sessions, or messages as CSV or JSON.
    Filtered by experiment_id when provided.
    """
    if table not in VALID_TABLES:
        raise HTTPException(status_code=400, detail=f"Invalid table. Choose from: {VALID_TABLES}")

    query: dict = {}

    if table == "participants":
        collection = db.participants
        if experiment_id:
            # Participants don't have experiment_id directly; get via sessions.
            # For simplicity, return all participants for now.
            pass
    elif table == "sessions":
        collection = db.chat_sessions
        if experiment_id:
            query["experiment_id"] = experiment_id
    else:  # messages
        collection = db.messages
        if experiment_id:
            # Join via chat_sessions — get session IDs first
            session_ids = await db.chat_sessions.distinct(
                "_id", {"experiment_id": experiment_id}
            )
            query["chat_session_id"] = {"$in": session_ids}

    cursor = collection.find(query).sort("created_at", 1)
    docs = await cursor.to_list(length=50_000)

    # Normalise _id → id
    for d in docs:
        if "_id" in d:
            d["id"] = str(d.pop("_id"))

    if format == "json":
        return docs

    if not docs:
        return Response(content="", media_type="text/csv")

    output = io.StringIO()
    fieldnames = list(docs[0].keys())
    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for row in docs:
        writer.writerow(row)

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{table}.csv"'},
    )
