# Intelligence Flow: RAG Converstaion

Intelligence Flow is a professional RAG (Retrieval-Augmented Generation) chatbot designed for analyzing PDF documents. It features a sleek, glassmorphic UI and uses advanced streaming responses to provide real-time intelligence from your documents.

## Features

*   **Interactive Chat Interface**: A modern, responsive chat tailored for document analysis.
*   **PDF Knowledge Base**: Upload multiple PDF documents to create a custom knowledge base.
*   **Streaming Responses**: Real-time answer generation using Groq's Llama 3 models.
*   **Context-Aware**: Maintains conversation history for follow-up questions.
*   **Professional UI**: Glassmorphism design with particle background effects.

## Technology Stack

*   **Frontend**: Streamlit
*   **LLM**: Llama 3.1-8b (via Groq)
*   **Embeddings**: HuggingFace (`all-MiniLM-L6-v2`)
*   **Vector Store**: ChromaDB
*   **Framework**: LangChain

## Prerequisites

*   Python 3.8+
*   A [Groq API Key](https://console.groq.com/)
*   A [Hugging Face Token](https://huggingface.co/settings/tokens)

## Installation

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a virtual environment**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You may need to create a requirements.txt file based on the imports in `server.py` common packages include: `streamlit`, `langchain`, `langchain-groq`, `langchain-huggingface`, `langchain-chroma`, `python-dotenv`, `pypdf`, `particles-js` support not needed via pip)*

4.  **Configure Environment**
    Create a `.env` file in the root directory and add your Hugging Face token:
    ```env
    HF_TOKEN=your_huggingface_token_here
    ```

## Usage

1.  **Run the application**
    ```bash
    streamlit run server.py
    ```

2.  **Open in Browser**
    The app will typically open at `http://localhost:8501`.

3.  **Start Chatting**
    *   Enter your **Groq API Key** in the sidebar.
    *   Upload one or more **PDF** documents.
    *   Ask questions in the chat input!


