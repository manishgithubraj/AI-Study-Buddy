# AI Study Buddy

Upload any study material (PDF or TXT) and get:
- Instant Q&A powered by RAG
- Auto-generated quizzes (easy/medium/hard)
- Flashcards for active recall
- Smart concept summaries

## Setup

```bash
# 1. Go into the folder
cd studybuddy

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 4. Install libraries
pip install -r requirements.txt

# 5. Add your Groq API key — create a .env file:
GROQ_API_KEY=gsk_xxxxxx

# 6. Run the app
streamlit run app.py
```

## Project Structure

```
studybuddy/
├── app.py           ← Main Streamlit UI (4 modes)
├── rag_engine.py    ← PDF reading + TF-IDF search
├── llm_engine.py    ← All Groq API calls
├── requirements.txt
└── .env             ← Your API key (don't share this)
```

## How it works

1. You upload a PDF or TXT file
2. rag_engine.py splits it into chunks and indexes with TF-IDF
3. When you ask a question, RAG finds the most relevant chunks
4. Those chunks + your question go to Groq (Llama 3.3)
5. The LLM answers, generates quizzes, or makes flashcards

## What you learn building this

- RAG pipeline from scratch (no LangChain needed)
- TF-IDF text search
- Streamlit multi-page apps with session state
- Groq API / LLM integration
- PDF text extraction with PyPDF2
