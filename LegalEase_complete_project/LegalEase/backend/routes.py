from fastapi import APIRouter, HTTPException
from backend.models import DocumentRequest
from backend.ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()
generator = GeminiDocumentGenerator()


@router.get("/health")
def health():
    return {"status": "ok", "service": "LegalEase API"}


@router.post("/generate")
def generate_document(request: DocumentRequest):
    try:
        document = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates,
        )
        return {
            "success": True,
            "document": document,
            "document_type": request.document_type,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
