"""
AI Study Buddy — Main Streamlit App
Upload study material → Ask questions, generate quizzes,
flashcards, and concept summaries powered by RAG + LLM.
"""

import streamlit as st
from rag_engine import StudyRAG, extract_text_from_pdf, extract_text_from_txt
from llm_engine import (
    answer_question, generate_quiz,
    generate_flashcards, generate_summary, explain_concept
)

# ── Page config ──────────────────────────────────────────
st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ───────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
}

.stApp {
    background: #0F0F13;
    color: #E8E6E0;
}

section[data-testid="stSidebar"] {
    background: #16161C;
    border-right: 1px solid #2A2A35;
}

.main-header {
    text-align: center;
    padding: 2rem 0 1rem;
}

.main-title {
    font-size: 2.8rem;
    font-weight: 600;
    color: #E8E6E0;
    letter-spacing: -1px;
    margin-bottom: 0.3rem;
}

.main-subtitle {
    font-size: 1rem;
    color: #6B6880;
    font-weight: 300;
}

.accent { color: #7C6AF7; }

.feature-card {
    background: #16161C;
    border: 1px solid #2A2A35;
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1rem;
}

.quiz-card {
    background: #16161C;
    border: 1px solid #2A2A35;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
}

.quiz-question {
    font-size: 1rem;
    font-weight: 500;
    color: #E8E6E0;
    margin-bottom: 1rem;
    line-height: 1.6;
}

.flashcard-front {
    background: #1E1E2A;
    border: 1px solid #7C6AF7;
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    font-size: 1.1rem;
    font-weight: 500;
    color: #E8E6E0;
    margin-bottom: 0.5rem;
    min-height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.flashcard-back {
    background: #1A2A1A;
    border: 1px solid #4CAF50;
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    font-size: 0.95rem;
    color: #B8E6B8;
    margin-bottom: 1rem;
    min-height: 80px;
}

.stat-box {
    background: #16161C;
    border: 1px solid #2A2A35;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}

.stat-num {
    font-size: 1.8rem;
    font-weight: 600;
    color: #7C6AF7;
    font-family: 'JetBrains Mono', monospace;
}

.stat-label {
    font-size: 0.75rem;
    color: #6B6880;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 2px;
}

.correct-badge {
    background: #1A3A1A;
    color: #4CAF50;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
}

.wrong-badge {
    background: #3A1A1A;
    color: #F44336;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
}

.chunk-badge {
    background: #1E1A3A;
    color: #7C6AF7;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.75rem;
    font-family: 'JetBrains Mono', monospace;
}

div[data-testid="stButton"] button {
    background: #7C6AF7;
    color: white;
    border: none;
    border-radius: 8px;
    font-family: 'Sora', sans-serif;
    font-weight: 500;
    transition: opacity 0.2s;
}

div[data-testid="stButton"] button:hover {
    background: #6A58E0;
    border: none;
}

.stTextInput input, .stTextArea textarea {
    background: #16161C;
    border: 1px solid #2A2A35;
    color: #E8E6E0;
    border-radius: 8px;
    font-family: 'Sora', sans-serif;
}

.stSelectbox select {
    background: #16161C;
    color: #E8E6E0;
}

.stRadio label {
    color: #E8E6E0 !important;
}

.stMarkdown p { color: #C8C6C0; }
.stMarkdown h2 { color: #E8E6E0; }
.stMarkdown h3 { color: #A8A6B8; }
.stMarkdown li { color: #C8C6C0; }

.upload-hint {
    text-align: center;
    color: #6B6880;
    font-size: 0.85rem;
    margin-top: 0.5rem;
}
</style>
""", unsafe_allow_html=True)


# ── Session state ────────────────────────────────────────
if "rag" not in st.session_state:
    st.session_state.rag = StudyRAG()
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = []
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}
if "flashcards" not in st.session_state:
    st.session_state.flashcards = []
if "fc_index" not in st.session_state:
    st.session_state.fc_index = 0
if "fc_show_back" not in st.session_state:
    st.session_state.fc_show_back = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ── Sidebar ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📚 Study Buddy")
    st.markdown("---")

    st.markdown("### Upload your material")
    uploaded = st.file_uploader(
        "PDF or TXT file",
        type=["pdf", "txt"],
        help="Upload your notes, textbook chapter, or any study material"
    )

    if uploaded:
        rag = st.session_state.rag
        if st.button("Process Document", use_container_width=True):
            with st.spinner("Reading and indexing..."):
                if uploaded.type == "application/pdf":
                    text = extract_text_from_pdf(uploaded)
                else:
                    text = extract_text_from_txt(uploaded)

                if text and not text.startswith("Error"):
                    n = rag.load_document(text, uploaded.name)
                    st.session_state.quiz_data = []
                    st.session_state.flashcards = []
                    st.session_state.chat_history = []
                    st.success(f"Indexed {n} chunks!")
                else:
                    st.error(text)

    st.markdown("---")

    if st.session_state.rag.is_loaded():
        doc = st.session_state.rag.doc_name
        n_chunks = len(st.session_state.rag.chunks)
        st.markdown(f"**Document:** {doc}")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""<div class="stat-box">
                <div class="stat-num">{n_chunks}</div>
                <div class="stat-label">Chunks</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            words = sum(len(c.split()) for c in st.session_state.rag.chunks)
            st.markdown(f"""<div class="stat-box">
                <div class="stat-num">{words//1000}k</div>
                <div class="stat-label">Words</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("Upload a document to get started.")

    st.markdown("---")
    st.markdown("**Mode**")
    mode = st.radio(
        "",
        ["Ask Questions", "Quiz Me", "Flashcards", "Summary"],
        label_visibility="collapsed"
    )


# ── Main area ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <div class="main-title">AI <span class="accent">Study</span> Buddy</div>
  <div class="main-subtitle">Upload your study material. Ask, quiz, flashcard, summarize.</div>
</div>
""", unsafe_allow_html=True)

rag = st.session_state.rag

if not rag.is_loaded():
    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    feats = [
        ("💬", "Ask Questions", "Ask anything about your material. RAG finds the right context."),
        ("🧠", "Quiz Generator", "Auto-generates MCQ questions at your chosen difficulty."),
        ("🃏", "Flashcards", "Front/back cards for active recall and spaced repetition."),
        ("📋", "Smart Summary", "Structured summary with key concepts and definitions."),
    ]
    for col, (icon, title, desc) in zip([c1, c2, c3, c4], feats):
        with col:
            st.markdown(f"""<div class="feature-card">
                <div style="font-size:1.8rem;margin-bottom:0.5rem">{icon}</div>
                <div style="font-weight:500;color:#E8E6E0;margin-bottom:0.4rem">{title}</div>
                <div style="font-size:0.82rem;color:#6B6880;line-height:1.5">{desc}</div>
            </div>""", unsafe_allow_html=True)
    st.markdown('<div class="upload-hint">👈 Upload a PDF or TXT file in the sidebar to begin</div>', unsafe_allow_html=True)
    st.stop()


# ════════════════════════════════════════════════════
# MODE 1 — ASK QUESTIONS
# ════════════════════════════════════════════════════
if mode == "Ask Questions":
    st.markdown("## 💬 Ask Questions")
    st.markdown(f"*Studying: **{rag.doc_name}***")

    # Chat history display
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    question = st.chat_input("Ask anything about your document...")

    if question:
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching document..."):
                results = rag.retrieve(question, top_k=5)
                context = rag.format_context(results)
                answer = answer_question(question, context, rag.doc_name)
            st.markdown(answer)

            if results:
                with st.expander(f"📄 Sources used ({len(results)} excerpts)"):
                    for r in results:
                        st.markdown(f'<span class="chunk-badge">Chunk #{r["chunk_id"]} · score {r["score"]}</span>', unsafe_allow_html=True)
                        st.markdown(f"> {r['text'][:200]}...")

        st.session_state.chat_history.append({"role": "assistant", "content": answer})

    if st.session_state.chat_history:
        if st.button("Clear chat"):
            st.session_state.chat_history = []
            st.rerun()


# ════════════════════════════════════════════════════
# MODE 2 — QUIZ
# ════════════════════════════════════════════════════
elif mode == "Quiz Me":
    st.markdown("## 🧠 Quiz Generator")

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        num_q = st.selectbox("Number of questions", [3, 5, 8, 10], index=1)
    with col2:
        difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"], index=1)
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        gen_quiz = st.button("Generate Quiz", use_container_width=True)

    if gen_quiz:
        with st.spinner(f"Generating {num_q} {difficulty} questions..."):
            context = rag.get_full_context(top_k=10)
            quiz = generate_quiz(context, num_q, difficulty)
            st.session_state.quiz_data = quiz
            st.session_state.quiz_answers = {}

    if st.session_state.quiz_data:
        st.markdown("---")
        correct = 0
        total = len(st.session_state.quiz_data)

        for i, q in enumerate(st.session_state.quiz_data):
            letters = ["A", "B", "C", "D"]
            options = [f"{letters[j]}. {opt}" for j, opt in enumerate(q["options"])]

            st.markdown(f"""<div class="quiz-card">
                <div class="quiz-question">Q{i+1}. {q['question']}</div>
            </div>""", unsafe_allow_html=True)

            answer_key = f"q_{i}"
            chosen = st.radio(
                f"q{i+1}",
                options,
                key=answer_key,
                label_visibility="collapsed"
            )
            st.session_state.quiz_answers[i] = chosen

            if chosen:
                chosen_idx = options.index(chosen)
                if chosen_idx == q["answer"]:
                    correct += 1
                    st.markdown('<span class="correct-badge">✓ Correct!</span>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<span class="wrong-badge">✗ Wrong — correct: {letters[q["answer"]]}. {q["options"][q["answer"]]}</span>', unsafe_allow_html=True)
                st.markdown(f"*{q['explanation']}*")

            st.markdown("")

        # Score summary
        if len(st.session_state.quiz_answers) == total:
            st.markdown("---")
            pct = int((correct / total) * 100)
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"""<div class="stat-box">
                    <div class="stat-num">{correct}/{total}</div>
                    <div class="stat-label">Score</div>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""<div class="stat-box">
                    <div class="stat-num">{pct}%</div>
                    <div class="stat-label">Accuracy</div>
                </div>""", unsafe_allow_html=True)
            with c3:
                grade = "A" if pct >= 90 else "B" if pct >= 75 else "C" if pct >= 60 else "F"
                st.markdown(f"""<div class="stat-box">
                    <div class="stat-num">{grade}</div>
                    <div class="stat-label">Grade</div>
                </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════
# MODE 3 — FLASHCARDS
# ════════════════════════════════════════════════════
elif mode == "Flashcards":
    st.markdown("## 🃏 Flashcards")

    col1, col2 = st.columns([3, 1])
    with col1:
        num_fc = st.selectbox("Number of flashcards", [5, 8, 10, 15], index=1)
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        gen_fc = st.button("Generate Cards", use_container_width=True)

    if gen_fc:
        with st.spinner("Creating flashcards..."):
            context = rag.get_full_context(top_k=10)
            cards = generate_flashcards(context, num_fc)
            st.session_state.flashcards = cards
            st.session_state.fc_index = 0
            st.session_state.fc_show_back = False

    if st.session_state.flashcards:
        cards = st.session_state.flashcards
        idx = st.session_state.fc_index
        total = len(cards)
        card = cards[idx]

        st.markdown("---")
        st.markdown(f"**Card {idx + 1} of {total}**")
        st.progress((idx + 1) / total)

        st.markdown(f'<div class="flashcard-front">{card["front"]}</div>', unsafe_allow_html=True)

        if st.session_state.fc_show_back:
            st.markdown(f'<div class="flashcard-back">{card["back"]}</div>', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col1:
            if st.button("◀ Prev") and idx > 0:
                st.session_state.fc_index -= 1
                st.session_state.fc_show_back = False
                st.rerun()
        with col2:
            if st.button("Reveal Answer" if not st.session_state.fc_show_back else "Hide Answer"):
                st.session_state.fc_show_back = not st.session_state.fc_show_back
                st.rerun()
        with col3:
            if st.button("Next ▶") and idx < total - 1:
                st.session_state.fc_index += 1
                st.session_state.fc_show_back = False
                st.rerun()
        with col4:
            if st.button("Shuffle"):
                import random
                random.shuffle(st.session_state.flashcards)
                st.session_state.fc_index = 0
                st.session_state.fc_show_back = False
                st.rerun()

        st.markdown("---")
        st.markdown("**All cards**")
        for i, c in enumerate(cards):
            with st.expander(f"Card {i+1}: {c['front'][:60]}..."):
                st.markdown(f"**Q:** {c['front']}")
                st.markdown(f"**A:** {c['back']}")


# ════════════════════════════════════════════════════
# MODE 4 — SUMMARY
# ════════════════════════════════════════════════════
elif mode == "Summary":
    st.markdown("## 📋 Smart Summary")
    st.markdown(f"*Document: **{rag.doc_name}***")

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("Generate Summary", use_container_width=True):
            with st.spinner("Analyzing and summarizing..."):
                context = rag.get_full_context(top_k=12)
                summary = generate_summary(context, rag.doc_name)
                st.session_state["summary"] = summary

    if "summary" in st.session_state:
        st.markdown(st.session_state["summary"])

        st.markdown("---")
        st.markdown("### Deep dive on a concept")
        concept = st.text_input("Enter a specific concept to explain in depth:")
        if concept and st.button("Explain this concept"):
            with st.spinner(f"Explaining '{concept}'..."):
                results = rag.retrieve(concept, top_k=4)
                context = rag.format_context(results)
                explanation = explain_concept(concept, context)
            st.markdown("---")
            st.markdown(explanation)
    else:
        st.info("Click 'Generate Summary' to create a structured overview of your document.")
