import os
import html
import requests
import streamlit as st

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.utils.document_formatter import format_docx, format_txt
from backend.utils.pdf_generator import format_pdf

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
)

API_URL = os.getenv("LEGALEASE_API_URL", "http://127.0.0.1:8000").rstrip("/")


def preview_html(text: str) -> str:
    safe = html.escape(text)
    safe = safe.replace("\n\n", "<br><br>").replace("\n", "<br>")
    return f"""
    <div style="
        background:#111827;
        color:#f9fafb;
        padding:24px;
        border-radius:14px;
        border:1px solid #374151;
        line-height:1.7;
        max-height:600px;
        overflow-y:auto;
        font-family:Georgia,serif;
        white-space:normal;">
        {safe}
    </div>
    """


st.markdown(
    """
    <style>
    .main-title {
        text-align:center;
        font-size:42px;
        font-weight:800;
        margin-bottom:0;
    }
    .subtitle {
        text-align:center;
        color:#6b7280;
        margin-bottom:25px;
    }
    .stButton > button {
        width:100%;
        border-radius:10px;
        font-weight:700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">⚖️ LegalEase</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-Powered Legal Document Generator</div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("About LegalEase")
    st.write(
        "Create structured legal-document drafts from your inputs, "
        "edit them, preview them, and export them."
    )
    st.warning(
        "LegalEase generates drafts for review. It does not replace advice "
        "from a qualified legal professional."
    )
    st.caption(f"Backend: {API_URL}")

left, right = st.columns(2)

with left:
    document_type = st.selectbox(
        "Document Type",
        [
            "Employment Contract",
            "Non-Disclosure Agreement (NDA)",
            "Lease Agreement",
            "Freelance Work Contract",
            "Service Agreement",
            "Offer Letter",
            "Partnership Agreement",
            "General Agreement",
            "Other",
        ],
    )

    if document_type == "Other":
        document_type = st.text_input(
            "Enter document type",
            placeholder="Example: Software Development Agreement",
        )

    parties = st.text_area(
        "Parties Involved",
        height=130,
        placeholder=(
            "Example:\n"
            "Jane Doe (Service Provider)\n"
            "TechNova Inc. (Client)"
        ),
    )

with right:
    dates = st.text_input(
        "Effective Date",
        placeholder="Example: 30 September 2026",
    )

    terms = st.text_area(
        "Terms & Conditions",
        height=180,
        placeholder=(
            "Enter each term separated by a semicolon (;)\n\n"
            "Payment within 30 days of invoice; "
            "Confidentiality must be maintained; "
            "Either party may terminate with 15 days notice"
        ),
    )

generate = st.button("✨ Generate Document", type="primary")

if generate:
    if not all(
        [
            document_type.strip(),
            parties.strip(),
            dates.strip(),
            terms.strip(),
        ]
    ):
        st.error("Please complete all fields before generating the document.")
    else:
        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "dates": dates,
        }

        with st.spinner("Generating your legal document..."):
            try:
                response = requests.post(
                    f"{API_URL}/generate",
                    json=payload,
                    timeout=180,
                )
                response.raise_for_status()
                data = response.json()
                st.session_state["document"] = data["document"]
                st.session_state["document_type"] = document_type
                st.session_state["terms"] = terms
                st.success("Document generated successfully.")
            except requests.RequestException as exc:
                st.error(
                    "Could not connect to the FastAPI backend. "
                    "Make sure the backend is running."
                )
                st.code(str(exc))
            except Exception as exc:
                st.error(f"Generation failed: {exc}")

if "document" in st.session_state:
    st.divider()
    st.subheader("Generated Document")

    edited = st.toggle("✏️ Edit Document", value=False)

    if edited:
        st.session_state["document"] = st.text_area(
            "Edit the document",
            value=st.session_state["document"],
            height=600,
        )
    else:
        st.markdown(
            preview_html(st.session_state["document"]),
            unsafe_allow_html=True,
        )

    current_text = st.session_state["document"]
    current_type = st.session_state.get("document_type", "Legal Document")
    current_terms = st.session_state.get("terms", "")

    st.subheader("Download")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.download_button(
            "⬇️ Download TXT",
            data=format_txt(current_text),
            file_name="legalease_document.txt",
            mime="text/plain",
        )

    with c2:
        st.download_button(
            "⬇️ Download DOCX",
            data=format_docx(current_text, current_type, current_terms),
            file_name="legalease_document.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    with c3:
        st.download_button(
            "⬇️ Download PDF",
            data=format_pdf(current_text, current_type),
            file_name="legalease_document.pdf",
            mime="application/pdf",
        )
