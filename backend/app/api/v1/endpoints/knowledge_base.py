"""
Knowledge base endpoints: list documents, add a manual entry (e.g. a
pricing plan), upload a PDF/DOCX/TXT, and delete a document.
"""
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.ai.providers.base import AIProvider
from app.ai.providers.factory import get_ai_provider
from app.api.deps import require_admin
from app.db.session import get_db
from app.knowledge_base.parsers import SUPPORTED_EXTENSIONS, get_extension
from app.schemas.knowledge_base import KnowledgeBaseDocumentRead, ManualEntryCreate
from app.services import knowledge_base_service

router = APIRouter(prefix="/knowledge-base", tags=["knowledge-base"], dependencies=[Depends(require_admin)])

MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10 MB


def _to_read_schema(document, chunk_count: int) -> KnowledgeBaseDocumentRead:
    return KnowledgeBaseDocumentRead(
        id=document.id,
        title=document.title,
        source_type=document.source_type,
        original_filename=document.original_filename,
        chunk_count=chunk_count,
        created_at=document.created_at,
    )


@router.get("", response_model=list[KnowledgeBaseDocumentRead])
def list_documents(db: Session = Depends(get_db)):
    rows = knowledge_base_service.list_documents(db)
    return [_to_read_schema(row["document"], row["chunk_count"]) for row in rows]


@router.post("/manual", response_model=KnowledgeBaseDocumentRead, status_code=201)
async def create_manual_entry(
    payload: ManualEntryCreate,
    db: Session = Depends(get_db),
    ai_provider: AIProvider = Depends(get_ai_provider),
):
    try:
        document = await knowledge_base_service.create_manual_entry(db, payload.title, payload.content, ai_provider)
    except Exception:
        raise HTTPException(status_code=502, detail="Failed to embed this entry - check your GEMINI_API_KEY and try again.")

    return _to_read_schema(document, len(document.chunks))


@router.post("/upload", response_model=KnowledgeBaseDocumentRead, status_code=201)
async def upload_document(
    file: UploadFile,
    db: Session = Depends(get_db),
    ai_provider: AIProvider = Depends(get_ai_provider),
):
    extension = get_extension(file.filename or "")
    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: .{extension}. Supported: PDF, DOCX, TXT.")

    content = await file.read()
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=400, detail="File is too large (10 MB limit).")

    try:
        document = await knowledge_base_service.create_uploaded_document(db, file.filename, content, ai_provider)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=502, detail="Failed to process/embed this file - check your GEMINI_API_KEY and try again.")

    return _to_read_schema(document, len(document.chunks))


@router.delete("/{document_id}", status_code=204)
def delete_document(document_id: uuid.UUID, db: Session = Depends(get_db)):
    document = knowledge_base_service.get_document(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    knowledge_base_service.delete_document(db, document)
