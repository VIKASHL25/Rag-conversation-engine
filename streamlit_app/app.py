import streamlit as st
import streamlit.components.v1 as components
import requests
import os
from dotenv import load_dotenv
from streamlit_lottie import st_lottie


from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.messages import HumanMessage, AIMessage


load_dotenv("../.env")
DJANGO_BASE_URL=os.getenv("DJANGO_BASE_URL")

query_params=st.query_params
session_key=query_params.get("session")

if not session_key:
    st.error("Unauthorized Access")
    st.stop()

response=requests.get(
    f"{DJANGO_BASE_URL}/validate-session/",params={"session":session_key}
)

if not response.json().get("valid"):
    st.error("Session Invalid")
    st.stop()

st.set_page_config(page_title="Intelligence Flow", page_icon="💎", layout="wide")

def apply_professional_ui():
    st.markdown("""
    <style>
    .main { background: transparent !important; }
    .stApp { background: #0b0e14; }
    
    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(15, 20, 30, 0.8) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Message Entry Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .stChatMessage {
        animation: fadeIn 0.4s ease-out forwards;
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 15px !important;
        margin-bottom: 1rem !important;
    }

    .hero-text {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(120deg, #ffffff, #64748b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0px;
    }
                
    .hero-text .emoji {
        -webkit-text-fill-color: initial;
        background: none;
    }
    .logout-container div.stButton > button {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
    }

    .logout-container div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(239, 68, 68, 0.5);
        background: linear-gradient(135deg, #dc2626, #b91c1c);
    }

    /* Clean Input */
    .stChatInputContainer { background: transparent !important; }
    </style>
    """, unsafe_allow_html=True)

    components.html("""
    <div id="particles-js" style="position:fixed; top:0; left:0; width:100vw; height:100vh; z-index:-1;"></div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
        particlesJS("particles-js", {
            "particles": {
                "number": {"value": 90, "density": {"enable": true, "value_area": 800}},
                "color": {"value": "#ffffff"},
                "shape": {"type": "circle"},
                "opacity": {"value": 0.2, "random": true},
                "size": {"value": 2, "random": true},
                "line_linked": {"enable": true, "distance": 150, "color": "#ffffff", "opacity": 0.1, "width": 1},
                "move": {"enable": true, "speed": 1.5}
            },
            "interactivity": {
                "events": {"onhover": {"enable": true, "mode": "grab"}}
            },
            "retina_detect": true
        });
    </script>
    """, height=0)

apply_professional_ui()


with st.sidebar:
    st.markdown('<div class="logout-container">', unsafe_allow_html=True)
    logout_clicked = st.button("Logout",key="logout_btn")
    st.markdown('</div>', unsafe_allow_html=True)

    if logout_clicked:
        st.markdown(f"[Click here to Logout]({DJANGO_BASE_URL}/logout/)")
        st.stop()

os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

embeddings = get_embeddings()

if "store" not in st.session_state:
    st.session_state.store = {}



with st.sidebar:
    st.markdown("### Workspace")
    api_key = st.text_input("Groq API Key", type="password")
    session_id = st.text_input("Session ID", value="pro_user_01")
    
    st.markdown("---")
    uploaded_files = st.file_uploader("Knowledge Base (PDF)", type="pdf", accept_multiple_files=True)
    
    if st.button("Reset Session",key="reset_btn"):
        st.session_state.store[session_id] = ChatMessageHistory()
        st.rerun()

st.markdown(
    '<h1 class="hero-text"><span class="emoji">⚡</span> IntelFlow – Conversational RAG System</h1>',
    unsafe_allow_html=True
)

st.markdown("<p style='text-align:center; color:#64748b; font-size:0.9rem;'>Streaming RAG Intelligence</p>", unsafe_allow_html=True)

if session_id in st.session_state.store:
    for msg in st.session_state.store[session_id].messages:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.markdown(msg.content)

user_input = st.chat_input("Analyze documents...")

if api_key:
    llm = ChatGroq(groq_api_key=api_key, model_name="llama-3.3-70b-versatile", streaming=True)

    def get_session_history(session: str) -> BaseChatMessageHistory:
        if session_id not in st.session_state.store:
            st.session_state.store[session_id] = ChatMessageHistory()
        return st.session_state.store[session_id]

    if uploaded_files:
        documents = []
        for file in uploaded_files:
            temp_path = f"./temp_{file.name}"
            with open(temp_path, "wb") as f:
                f.write(file.getvalue())
            loader = PyPDFLoader(temp_path)
            documents.extend(loader.load())

        splits = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150).split_documents(documents)
        vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

        context_q_prompt = ChatPromptTemplate.from_messages([
            ("system", "Rewrite the user question to be standalone."),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ])

        history_aware_retriever = (
            {"input": lambda x: x["input"], "chat_history": lambda x: x["chat_history"]}
            | context_q_prompt | llm | StrOutputParser() | retriever
        )

        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", "Professional Assistant. Use context:\n\n{context}"),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ])

        rag_chain = (
            {"context": history_aware_retriever, "input": lambda x: x["input"], "chat_history": lambda x: x["chat_history"]}
            | qa_prompt | llm
        )

        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain, get_session_history,
            input_messages_key="input", history_messages_key="chat_history"
        )

        if user_input:
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                def stream_generator():
                    for chunk in conversational_rag_chain.stream(
                        {"input": user_input},
                        config={"configurable": {"session_id": session_id}}
                    ):
                        if hasattr(chunk, "content"):
                            yield chunk.content
                        elif isinstance(chunk, str):
                            yield chunk


                response_text = st.write_stream(stream_generator())
                
    else:
        if user_input:
            st.info("Please upload PDFs to begin.")
else:
    if user_input:
        st.warning("Please enter your Groq API Key.")
        