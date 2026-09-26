import os
import sys
import subprocess

# --- AUTOMATED CLOUD DEPENDENCY INSTALLER ---
try:
    import langchain
    import langchain_groq
except ModuleNotFoundError:
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", 
        "streamlit", "langchain", "langchain-groq", "langchain-community", "duckduckgo-search", "pypdf"
    ])

import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# --- FIX: MODERN, STANDARDIZED CORE IMPORTS ---
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import tool

# --- 1. UI CONFIGURATION & INTERFACE ---
st.set_page_config(page_title="Gnostic AI", page_icon="🧘", layout="wide")
st.title("🧘 Gnostic AI: The Esoteric Synthesis Master")
st.caption("Hosted on Cloud — Decoding Manifestation, Subconscious Reprogramming, and Scripture.")

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.3-70b-versatile", 
    groq_api_key=GROQ_API_KEY,
    temperature=0.5
)

web_search_engine = DuckDuckGoSearchRun()

# --- 2. DEFINE MODERN TOOLS WITH DECORATORS ---
@tool
def search_the_live_web(query: str) -> str:
    """Useful when you need to pull live philosophy articles, scripture cross-references, or web data."""
    return web_search_engine.run(query)

@tool
def read_local_spiritual_library(query: str) -> str:
    """Useful to scan books or PDFs uploaded locally in the data/ folder if running locally."""
    try:
        loader = PyPDFDirectoryLoader("data/")
        docs = loader.load()
        if not docs:
            return "Local data folder is empty."
        return " ".join([d.page_content for d in docs if query.lower() in d.page_content.lower()][:3])
    except:
        return "Could not read files."

tools = [search_the_live_web, read_local_spiritual_library]

# --- 3. MASTER PROMPT ENGINE ---
system_prompt = """You are Gnostic AI—an enlightened Spiritual Master, Esoteric Scholar, and Mystic Sage. 
Decode Manifestation, Subconscious Reprogramming, and Masculine Energy Cultivation.
Conclude every single answer with a clear, bulleted 'Daily Practical Blueprint' or 'Actionable Protocol' for modern life.
Translate ancient terms into clear modern psychological concepts."""

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_tool_calling_agent(llm, tools, prompt_template)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Namaste. I am Gnostic AI. What shall we master today?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if user_query := st.chat_input("Ask Gnostic AI..."):
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            try:
                response = agent_executor.invoke({"input": user_query, "chat_history": st.session_state.chat_history})
                output_text = response["output"]
                st.write(output_text)
                st.session_state.messages.append({"role": "assistant", "content": output_text})
                st.session_state.chat_history.append(("human", user_query))
                st.session_state.chat_history.append(("assistant", output_text))
            except Exception as e:
                st.error(f"Error: {e}")
