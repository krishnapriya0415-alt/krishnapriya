from google import genai
from google.genai import types

from backend.config import GEMINI_API_KEY, GEMINI_MODEL, DEMO_MODE


class GeminiDocumentGenerator:
    """Generates structured legal-document drafts using the Gemini API."""

    def __init__(self):
        self.client = None
        if GEMINI_API_KEY:
            self.client = genai.Client(api_key=GEMINI_API_KEY)

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str,
    ) -> str:
        if not self.client:
            if DEMO_MODE:
                return self._demo_document(document_type, parties, terms, dates)
            raise RuntimeError(
                "GEMINI_API_KEY is not configured. Add it to your .env file "
                "or set DEMO_MODE=true for a local demo without Gemini."
            )

        prompt = f"""
Create a professional legal document draft.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

EFFECTIVE DATE / DATES:
{dates}

TERMS AND CONDITIONS:
{terms}

Requirements:
1. Produce only the document draft, not commentary about how you generated it.
2. Use a clear title and numbered sections.
3. Include the parties, effective date, scope/purpose, obligations, payment or
   consideration where relevant, confidentiality where relevant, termination,
   dispute/governing-law placeholders where appropriate, notices, signatures,
   and any other clauses naturally required by the document type.
4. Do not invent sensitive facts, addresses, registration numbers, laws, fees,
   or obligations that the user did not provide. Use [TO BE COMPLETED] when
   necessary.
5. Preserve the user's supplied terms faithfully while improving organization
   and legal drafting style.
6. This is a draft for review, not legal advice. Include a short neutral
   "DRAFT NOTICE" at the end.
7. Do not use markdown tables. Use headings and paragraphs so the document can
   be exported cleanly to DOCX/PDF.
"""

        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.35,
                max_output_tokens=8000,
            ),
        )

        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text.strip()

    @staticmethod
    def _demo_document(document_type, parties, terms, dates):
        term_lines = []
        for item in terms.split(";"):
            item = item.strip()
            if item:
                term_lines.append(f"- {item}")

        return f"""DRAFT {document_type.upper()}

Effective Date: {dates}

PARTIES
{parties}

1. PURPOSE
This draft {document_type.lower()} records the understanding between the
parties identified above and is based on the information supplied by the user.

2. AGREED TERMS
{chr(10).join(term_lines) if term_lines else "- [TO BE COMPLETED]"}

3. RESPONSIBILITIES
Each party shall perform the responsibilities expressly assigned to it in the
final reviewed agreement.

4. CONFIDENTIALITY
Where confidential information is exchanged, the parties should use reasonable
measures to protect it and should document any confidentiality obligations in
the final agreement.

5. TERMINATION
The parties should specify the permitted termination events, notice period,
and consequences of termination before signing the final version.

6. GOVERNING LAW AND DISPUTES
[TO BE COMPLETED: applicable governing law, jurisdiction, and dispute process.]

7. ENTIRE AGREEMENT
The final signed document should contain the complete understanding of the
parties and identify any amendments or attachments.

8. SIGNATURES

Party 1: ______________________________
Name: __________________________________
Date: __________________________________

Party 2: ______________________________
Name: __________________________________
Date: __________________________________

DRAFT NOTICE
This document is an AI-generated draft for review and is not legal advice.
A qualified legal professional should review the final document before use or
signature.
"""
