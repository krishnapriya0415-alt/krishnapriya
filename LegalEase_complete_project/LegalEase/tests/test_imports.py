def test_backend_imports():
    from backend.main import app
    from backend.routes import router
    from backend.ai_core.gemini_generator import GeminiDocumentGenerator
    assert app is not None
    assert router is not None
    assert GeminiDocumentGenerator is not None
