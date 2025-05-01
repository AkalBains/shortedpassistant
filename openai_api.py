from __future__ import annotations
"""openai_api.py – GPT wrapper
--------------------------------------------------
Combines your original narrative guidelines with the new **strict‑JSON**
output requirement so that the rest of the pipeline can `json.loads()` the
reply without post‑processing.

Public helper
-------------
generate_report(raw_notes: str) -> str  # JSON string

Dependencies
------------
• `openai>=1.0.0`  (official SDK – already in requirements.txt)
• `backoff`        (simple retry decorator)
• `python-dotenv`  (so the same code works locally and on Streamlit Cloud)

Add `backoff` to your **requirements.txt** if it isn’t there yet.
"""

from pathlib import Path
import os
import json
import logging
from typing import List, Dict

import backoff  # type: ignore
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Prompt engineering – combines *your* instructions + strict JSON schema
# ---------------------------------------------------------------------------

_NARRATIVE_INSTRUCTIONS = """
System Purpose:\n\nYou are a professional report generator specialising in transforming structured input data into well‑written reports for a leadership consulting firm.\n\nBelow are details on the inputs you will receive and the outputs you should produce.\n\nInputs:\n1. 'Personal Profile': bullet point notes on the individual's distinctive psychology and their drivers and motivations in life.\n2. 'Strengths': three titles and explanatory bullet points on the individual's strengths.\n3. 'Development Areas': three titles and explanatory bullet points on the individual's development areas.\n4. 'Future Considerations': bullet points on where the individual wants their career to go, their capability, and what they need to do to get there.\n\nOutputs:\nProduce a full draft report following this structure and length guidance (word limits are *guidelines*, not hard caps):\n• Personal Profile (≈75–100 words) – two‑part paragraph.\n• Strengths (≈170–200 words total) – three sections using the original titles.\n• Development Areas (≈170–200 words total) – three sections using the original titles.\n• Future Considerations (≈75–100 words).\n• Personal Development Suggestions – two titled suggestions, each 40–65 words.\n• How the Organisation can Support Them – two titled suggestions, each 40–65 words.\n\nStyle:\nYour tone must mirror the four example reports provided to the model: professional, concise, psychological, and developmental. Expand and re‑phrase the consultant's bullets; do **not** copy them verbatim.\n"""

_JSON_REQUIREMENT = """
IMPORTANT – OUTPUT FORMAT:\nReturn *only* a single valid JSON object with exactly these keys. **Do not** wrap it in Markdown back‑ticks, and do not add comments or additional fields.\n\n{
  "personal_profile": string,
  "strengths": [
    {"title": string, "paragraph": string},
    {"title": string, "paragraph": string},
    {"title": string, "paragraph": string}
  ],
  "development_areas": [
    {"title": string, "paragraph": string},
    {"title": string, "paragraph": string},
    {"title": string, "paragraph": string}
  ],
  "future_considerations": string,
  "personal_development": [
    {"title": string, "paragraph": string},
    {"title": string, "paragraph": string}
  ],
  "org_support": [
    {"title": string, "paragraph": string},
    {"title": string, "paragraph": string}
  ]
}\n"""

SYSTEM_PROMPT = f"{_NARRATIVE_INSTRUCTIONS}\n\n{_JSON_REQUIREMENT}"

# ---------------------------------------------------------------------------
# Helper – single call with automatic back‑off and lightweight validation
# ---------------------------------------------------------------------------

def _chat(messages: List[Dict]) -> str:
    """Low‑level wrapper. Returns raw assistant text."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY missing – set it in .env or Streamlit secrets")

    client = OpenAI(api_key=api_key)

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3,
        max_tokens=1024,
    )
    return resp.choices[0].message.content.strip()


@backoff.on_exception(backoff.expo, (
    RuntimeError,
    Exception,  # broad – covers RateLimitError, APIError, etc. in openai>=1.0
), max_tries=3, jitter=backoff.full_jitter)
def generate_report(raw_notes: str) -> str:
    """Generate the narrative JSON for the leadership report.

    Parameters
    ----------
    raw_notes : str
        The consultant's bullet‑point notes pasted from the Streamlit form.

    Returns
    -------
    str
        A JSON string that adheres to the schema in `SYSTEM_PROMPT`.
    """
    if not raw_notes.strip():
        raise ValueError("raw_notes is empty – nothing to send to GPT")

    msgs = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": raw_notes},
    ]

    assistant_text = _chat(msgs)

    # quick parse check – if it fails, ask the model to fix its JSON once
    try:
        json.loads(assistant_text)
    except json.JSONDecodeError as err:
        logging.warning("OpenAI returned invalid JSON; asking for fix: %s", err)
        msgs.append({"role": "assistant", "content": assistant_text})
        msgs.append({"role": "user", "content": "That was not valid JSON. Please return *only* valid JSON."})
        assistant_text = _chat(msgs)

    return assistant_text
