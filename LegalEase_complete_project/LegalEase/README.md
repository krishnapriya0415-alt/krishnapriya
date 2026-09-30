# LegalEase - AI-Powered Legal Document Generator

LegalEase is a student-friendly Generative AI project that uses Streamlit,
FastAPI and Google's Gemini API to generate editable legal-document drafts.

## Features

- Employment contracts
- NDAs
- Lease agreements
- Freelance contracts
- Service agreements
- Offer letters
- Custom document types
- Editable generated text
- TXT export
- DOCX export
- PDF export
- FastAPI API
- Gemini AI integration
- Demo mode without an API key

## Project structure

```text
LegalEase/
├── backend/
│   ├── main.py
│   ├── routes.py
│   ├── models.py
│   ├── config.py
│   ├── ai_core/
│   │   └── gemini_generator.py
│   └── utils/
│       ├── document_formatter.py
│       ├── pdf_generator.py
│       └── text_utils.py
├── frontend/
│   └── app.py
├── .env
├── .env.example
├── requirements.txt
├── Procfile
├── Dockerfile
└── README.md
```

## Windows setup

Open this project folder in VS Code.

### 1. Create a virtual environment

```powershell
python -m venv .venv
```

### 2. Activate it

PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Command Prompt:

```cmd
.venv\Scripts\activate
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Add your Gemini API key

Open `.env` and change:

```text
GEMINI_API_KEY=
```

to:

```text
GEMINI_API_KEY=YOUR_REAL_API_KEY
```

Do not share your API key publicly.

### 5. Start FastAPI

Terminal 1:

```powershell
uvicorn backend.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

Open:

```text
http://127.0.0.1:8000/docs
```

to see the API documentation.

### 6. Start Streamlit

Open a second VS Code terminal:

```powershell
streamlit run frontend/app.py
```

Streamlit normally opens:

```text
http://localhost:8501
```

## Test without Gemini

If you do not have an API key yet, change:

```text
DEMO_MODE=true
```

Then restart the FastAPI server.

The application will generate a sample document locally so you can test
the complete frontend, editing and download workflow.

## Test the API manually

Use the FastAPI Swagger page at:

```text
http://127.0.0.1:8000/docs
```

Call POST `/generate` with:

```json
{
  "document_type": "Freelance Work Contract",
  "parties": "Jane Doe (Service Provider), TechNova Inc. (Client)",
  "terms": "Payment within 30 days; Confidentiality must be maintained; Either party may terminate with 15 days notice",
  "dates": "30 September 2026"
}
```

## Important

LegalEase produces AI-generated drafts and should not be treated as a
substitute for professional legal advice. Review generated documents before
using or signing them.
