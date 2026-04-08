:

📚 AI Study Buddy — Smart Learning Assistant

AI Study Buddy is an intelligent AI-powered learning companion designed to help students study more effectively. It provides real-time answers, simplifies complex concepts, generates summaries, and creates quizzes to enhance understanding and retention.

Built using modern NLP and Retrieval-Augmented Generation (RAG), the system delivers accurate, context-aware responses in an interactive and user-friendly interface.


🚀 Features
💬 Interactive Q&A — Ask questions from any subject
🧠 Concept Simplification — Complex topics explained simply
📝 Auto Notes Generation — Get clean and structured notes
📂 Document-Based Learning — Upload PDFs/text for analysis
❓ Quiz Generation — Test your knowledge instantly
⚡ Fast Responses — Real-time AI-powered answers
🎯 Personalized Learning — Tailored explanations


🛠️ Tech Stack
Language: Python
Frontend: Streamlit
AI/NLP: LLM APIs (OpenAI / Groq / Gemini)
Architecture: Retrieval-Augmented Generation (RAG)
Vector Database: FAISS / ChromaDB
Other Tools: dotenv, pathlib


📂 Project Structure
AI-Study-Buddy/
│
├── app.py
├── rag_engine.py
├── utils/
├── data/
├── requirements.txt
└── README.md



⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/your-username/ai-study-buddy.git
cd ai-study-buddy



2️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows


3️⃣ Install dependencies
pip install -r requirements.txt



4️⃣ Add environment variables

Create a .env file:

API_KEY=your_api_key_here
5️⃣ Run the app
streamlit run app.py



🧠 How It Works
User inputs a question or uploads study material
Text is converted into embeddings
Relevant data is retrieved using vector search
LLM generates a structured response
Output is displayed in the UI
📸 Use Cases
📖 Exam preparation
🧾 Quick revision notes
🧠 Concept clarity
🎓 Self-learning assistant
📊 Academic support tool
⭐ Reviews & Feedback

💬 “AI Study Buddy makes learning so much easier by breaking down complex topics into simple explanations.”

💬 “The quiz feature really helps in quick self-assessment before exams.”

💬 “Clean UI and fast responses — perfect for daily study use.”

📢 Share Your Feedback

If you like this project, consider:

⭐ Starring the repository
🐛 Reporting issues
💡 Suggesting new features
🔮 Future Enhancements
Voice-based interaction 🎙️
Multi-language support 🌍
Personalized study plans 📅
Performance tracking dashboard 📊
LMS integration
🤝 Contributing

Contributions are welcome!
Fork the repo and submit a pull request.

📜 License

MIT License

👨‍💻 Author

Manish Raj
📧 manishraj20526@gmail.com

🔗 linkedin.com/in/manishraj20526
