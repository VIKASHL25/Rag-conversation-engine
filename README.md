# 💎 IntelFlow – Conversational RAG Intelligence System

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2+-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-🦜-black?style=for-the-badge)](https://www.langchain.com/)
[![Groq](https://img.shields.io/badge/Groq-⚡-orange?style=for-the-badge)](https://groq.com/)

**IntelFlow** is a professional-grade, full-stack Conversational RAG (Retrieval-Augmented Generation) system. It combines a robust **Django** backend for secure session management and authentication with a state-of-the-art **Streamlit** frontend featuring a premium glassmorphic UI. The system allows users to upload PDF documents and engage in context-aware, history-persistent conversations powered by the **Llama-3.3-70B** model via Groq.

---

## Key Features

- **Hybrid Authentication System**: 
  - Django-powered user registration and login.
  - Email verification via SMTP.
  - Secure session-based cross-platform validation between Django and Streamlit.
- **Advanced RAG Engine**:
  - PDF document ingestion and processing using `PyPDF` and `LangChain`.
  - Contextual chunking with `RecursiveCharacterTextSplitter`.
  - History-aware retrieval for seamless multi-turn conversations.
- **High-Performance Inference**:
  - Integration with **Groq Cloud** for lightning-fast LLM responses (Llama-3.3-70B).
  - Streaming responses for an interactive chat experience.
- **Intelligent Data Store**:
  - Local vector storage using **ChromaDB**.
  - Embedding generation using HuggingFace's `all-MiniLM-L6-v2`.

---

## Tech Stack

### Frontend (UI/UX)
- **Streamlit**: Core web framework.

### Backend (Security & Logic)
- **Django**: User management, Authentication, and Session API.
- **MongoDB (Djongo)**: Primary database for user records and sessions.

### AI/ML (Intelligence)
- **LangChain**: Orchestration of RAG pipelines and chat history.
- **Groq API**: LLM provider (Inference).
- **HuggingFace Embeddings**: Vector representation of text.
- **ChromaDB**: Vector database for document retrieval.

---

## Project Structure

```bash
├── backend/                # Django Backend
│   ├── accounts/           # User Authentication & Custom User Model
│   ├── backend/            # Project Core Settings & URLs
│   ├── manage.py           # Django CLI
│   └── requirements.txt    # Backend Dependencies
├── streamlit_app/          # Streamlit Frontend
│   ├── app.py              # Main Streamlit Application
│   ├── requirements.txt    # Frontend Dependencies
│   └── runtime.txt         # Environment configuration
├── templates/              # HTML Templates for Django
├── static/                 # Static Assets
├── .env                    # System-wide Environment Variables
└── README.md               # Documentation
```

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Q_AConverstion
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory:
```env
# Django Settings
SECRET_KEY=your_django_secret_key
DEBUG=True
DJANGO_BASE_URL=http://127.0.0.1:8000
STREAMLIT_BASE_URL=http://localhost:8501

# Email Settings (SMTP)
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# AI Settings
HF_TOKEN=your_huggingface_token
```

### 3. Setup Backend (Django)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### 4. Setup Frontend (Streamlit)
```bash
cd streamlit_app
pip install -r requirements.txt
streamlit run app.py
```

---

## Usage

1. **Register**: Start at the Django login page (`http://127.0.0.1:8000/register/`).
2. **Verify**: Check your email and click the verification link.
3. **Login**: Login to be redirected to the IntelFlow dashboard.
4. **Configure**: Enter your **Groq API Key** in the sidebar.
5. **Upload**: Drop your PDF files into the "Knowledge Base" uploader.
6. **Chat**: Start asking questions about your documents in the glassmorphic chat interface.

---

## Security
- **Email Verification**: Ensures valid user accounts.
- **Session Bridge**: The Streamlit interface is only accessible via a valid Django session key, preventing unauthorized access.
- **API Privacy**: Uses environment variables for all sensitive keys (LLM, SMTP, DB).

---


---
*Developed with ❤️ using Generative AI and Modern Web Technologies.*
