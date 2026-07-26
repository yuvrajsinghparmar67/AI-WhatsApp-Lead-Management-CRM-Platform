"""
Orchestrates the knowledge base: turns a manual entry or an uploaded
PDF/DOCX/TXT file into a document + embedded chunks, and lists/deletes
documents. Mirrors ai_pipeline_service's role for messages - this is the
only place that ties parsing, chunking, and embedding together for
company knowledge.

Unlike the auto-triggered message analysis pipeline (which fails soft so
a flaky AI call never blocks a customer message), embedding failures here
are allowed to raise: an admin uploading a document needs to know it
didn't actually get indexed, rather than silently having an unsearchable
"ghost" document sit in the list.
"""
import uuid

from sqlalchemy.orm import Session

from app.ai.embeddings.embedding_service import embed_text
from app.ai.providers.base import AIProvider
from app.knowledge_base.chunking import chunk_text
from app.knowledge_base.parsers import extract_text, get_extension
from app.models.knowledge_base import KnowledgeBaseChunk, KnowledgeBaseDocument


async def _create_document_with_chunks(
    db: Session, title: str, source_type: str, original_filename: str | None, text: str, provider: AIProvider
) -> KnowledgeBaseDocument:
    document = KnowledgeBaseDocument(
        id=uuid.uuid4(), title=title, source_type=source_type, original_filename=original_filename
    )
    db.add(document)
    db.flush()  # assigns document.id without committing yet

    for index, chunk in enumerate(chunk_text(text)):
        embedding = await embed_text(chunk, provider)
        db.add(
            KnowledgeBaseChunk(
                id=uuid.uuid4(),
                document_id=document.id,
                chunk_index=index,
                content=chunk,
                embedding=embedding,
            )
        )

    db.commit()
    db.refresh(document)
    return document


async def create_manual_entry(db: Session, title: str, content: str, provider: AIProvider) -> KnowledgeBaseDocument:
    return await _create_document_with_chunks(db, title=title, source_type="manual", original_filename=None, text=content, provider=provider)


async def create_uploaded_document(
    db: Session, filename: str, content: bytes, provider: AIProvider
) -> KnowledgeBaseDocument:
    text = extract_text(filename, content)  # raises ValueError on unsupported type / empty file
    source_type = get_extension(filename)
    title = filename.rsplit(".", 1)[0]
    return await _create_document_with_chunks(
        db, title=title, source_type=source_type, original_filename=filename, text=text, provider=provider
    )


def list_documents(db: Session) -> list[dict]:
    documents = db.query(KnowledgeBaseDocument).order_by(KnowledgeBaseDocument.created_at.desc()).all()
    return [{"document": doc, "chunk_count": len(doc.chunks)} for doc in documents]


def get_document(db: Session, document_id) -> KnowledgeBaseDocument | None:
    return db.query(KnowledgeBaseDocument).filter(KnowledgeBaseDocument.id == document_id).first()


def delete_document(db: Session, document: KnowledgeBaseDocument) -> None:
    db.delete(document)  # cascades to chunks via the ORM relationship + DB-level ON DELETE CASCADE
    db.commit()
