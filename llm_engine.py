"""
Study Buddy LLM Engine
All AI-powered features: Q&A, quiz generation,
flashcards, and concept summaries — powered by Groq.
"""

import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


def _call(system: str, user: str, max_tokens: int = 1024) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
    )
    return response.choices[0].message.content


def answer_question(question: str, context: str, doc_name: str) -> str:
    """Answer a question based on retrieved context."""
    system = f"""You are an expert study assistant helping a student understand their study material from "{doc_name}".
Answer the question clearly and accurately using ONLY the provided excerpts.
If the answer is not in the excerpts, say so honestly.
Use simple language. Give examples where helpful. Keep the answer focused."""

    user = f"""Excerpts from the document:
{context}

Student's question: {question}

Please answer clearly based on the excerpts above."""

    return _call(system, user, max_tokens=800)


def generate_quiz(context: str, num_questions: int = 5, difficulty: str = "medium") -> list[dict]:
    """Generate multiple choice quiz questions from content."""
    system = """You are an expert educator creating quiz questions.
You MUST respond with ONLY a valid JSON array. No explanation, no markdown, no extra text.
Each question object must have exactly these keys:
- "question": the question text
- "options": array of exactly 4 strings (A, B, C, D options without letters)
- "answer": index of correct option (0, 1, 2, or 3)
- "explanation": brief explanation of why the answer is correct"""

    user = f"""Create {num_questions} {difficulty}-difficulty multiple choice questions from this content:

{context}

Return ONLY a JSON array like this:
[{{"question": "...", "options": ["opt1","opt2","opt3","opt4"], "answer": 0, "explanation": "..."}}]"""

    raw = _call(system, user, max_tokens=2000)

    # Parse JSON safely
    try:
        json_match = re.search(r'\[.*\]', raw, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception:
        pass
    return []


def generate_flashcards(context: str, num_cards: int = 8) -> list[dict]:
    """Generate front/back flashcards from content."""
    system = """You are an expert educator creating flashcards for active recall.
You MUST respond with ONLY a valid JSON array. No explanation, no markdown, no extra text.
Each flashcard object must have exactly these keys:
- "front": the question or term (short, clear)
- "back": the answer or definition (concise but complete)"""

    user = f"""Create {num_cards} flashcards from this study content:

{context}

Return ONLY a JSON array like this:
[{{"front": "What is X?", "back": "X is..."}}]"""

    raw = _call(system, user, max_tokens=1500)

    try:
        json_match = re.search(r'\[.*\]', raw, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception:
        pass
    return []


def generate_summary(context: str, doc_name: str) -> str:
    """Generate a structured concept summary of the document."""
    system = """You are an expert study assistant creating a clear, structured summary.
Format your response with these sections using markdown:
## Key Concepts
## Main Ideas  
## Important Definitions
## Quick Review Points

Keep each section concise and student-friendly."""

    user = f"""Create a structured study summary of this content from "{doc_name}":

{context}"""

    return _call(system, user, max_tokens=1200)


def explain_concept(concept: str, context: str) -> str:
    """Give a deep-dive explanation of a specific concept."""
    system = """You are an expert tutor explaining concepts to a student.
Explain clearly using:
1. Simple definition
2. Real-world analogy
3. Key points to remember
4. Example if applicable

Be engaging and easy to understand."""

    user = f"""Using this context:
{context}

Explain this concept in depth: {concept}"""

    return _call(system, user, max_tokens=700)
