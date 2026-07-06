import time
import uuid
import logging

from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.config import settings
from app.models.chat import ChatSession, ChatMessage
from app.services.retrieval import retrieve_relevant_chunks
from app.services.prompt import build_messages
from app.services.llm import call_llm, LLMError
from app.services.local_assistant import answer_from_local_knowledge, answer_from_retrieved_chunks

logger = logging.getLogger("lenspilot")
router = APIRouter()


# ---------- Schemas (this is the API contract -- keep in sync with docs/API.md) ----------

class ChatRequest(BaseModel):
    session_id: str | None = Field(default=None, description="Existing session id, or omit to start a new one")
    message: str = Field(..., min_length=1, description="The user's question")


class Source(BaseModel):
    document_id: int
    document_title: str
    category: str
    audience: str
    source: str
    similarity: float


class ChatResponse(BaseModel):
    reply: str
    sources: list[Source]
    session_id: str


# ---------- Simple optional API-key auth ----------

def verify_api_key(
    x_api_key: str | None = Header(default=None),
    authorization: str | None = Header(default=None),
):
    bearer_token = None
    if authorization and authorization.lower().startswith("bearer "):
        bearer_token = authorization[7:].strip()

    if settings.API_KEY and settings.API_KEY not in (x_api_key, bearer_token):
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return True


# ---------- Routes ----------

@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db), _auth=Depends(verify_api_key)):
    start = time.time()
    session_id = payload.session_id or str(uuid.uuid4())

    # Make sure the session exists (create if new) -- best effort, chat still works if this fails
    try:
        session = db.get(ChatSession, session_id)
        if session is None:
            session = ChatSession(id=session_id)
            db.add(session)
            db.commit()
    except Exception:
        db.rollback()
        logger.exception("Could not persist chat session %s", session_id)

    local_result = answer_from_local_knowledge(payload.message, db)
    if local_result is not None:
        reply_text = local_result.reply
        chunks = local_result.sources
        logger.info("Answered from local LensPilot knowledge in %.2fs", time.time() - start)
    else:
        chunks = []

    # 1. Retrieve relevant chunks
    if local_result is None:
        try:
            t0 = time.time()
            chunks = retrieve_relevant_chunks(db, payload.message)
            logger.info("Retrieved %d chunks in %.2fs", len(chunks), time.time() - t0)
        except Exception:
            logger.exception("Retrieval failed")
            raise HTTPException(
                status_code=503,
                detail="Knowledge lookup is temporarily unavailable. Please try again shortly.",
            )

        # 2. Build prompt + call LLM
        try:
            messages = build_messages(payload.message, chunks)
            t0 = time.time()
            reply_text = call_llm(messages)
            logger.info("LLM responded in %.2fs", time.time() - t0)
        except LLMError as e:
            fallback = answer_from_retrieved_chunks(payload.message, chunks)
            if fallback is not None:
                reply_text = fallback.reply
                chunks = fallback.sources
                logger.warning("LLM failed (%s); returned grounded local fallback", e.status_code)
            else:
                raise HTTPException(status_code=e.status_code, detail=str(e))
        except Exception:
            logger.exception("Unexpected LLM failure")
            raise HTTPException(status_code=500, detail="Something went wrong generating a response.")

    # 3. Persist messages (best effort)
    try:
        db.add(ChatMessage(session_id=session_id, role="user", content=payload.message))
        db.add(ChatMessage(session_id=session_id, role="assistant", content=reply_text))
        db.commit()
    except Exception:
        db.rollback()
        logger.exception("Could not persist chat messages for session %s", session_id)

    logger.info("Total /chat time: %.2fs", time.time() - start)

    return ChatResponse(
        reply=reply_text,
        sources=[
            Source(
                document_id=c["document_id"],
                document_title=c["document_title"],
                category=c["category"],
                audience=c["audience"],
                source=c["source"],
                similarity=c["similarity"],
            )
            for c in chunks
        ],
        session_id=session_id,
    )


@router.post("/ingest")
def trigger_ingest(_auth=Depends(verify_api_key)):
    """
    Manually trigger (re)ingestion of the docs in INGESTION_DOCS_DIR.
    Intended for admin/dev use -- for large doc sets prefer running
    `python ingestion/ingest.py` directly instead of over HTTP.
    """
    from ingestion.ingest import run_ingestion

    try:
        summary = run_ingestion()
        return {"status": "ok", **summary}
    except Exception:
        logger.exception("Ingestion failed")
        raise HTTPException(
            status_code=500,
            detail="Ingestion failed. Check the server logs for details.",
        )
