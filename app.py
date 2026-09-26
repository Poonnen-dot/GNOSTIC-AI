import os
import sys
import subprocess

# --- AUTOMATED CLOUD DEPENDENCY INSTALLER ---
# Forces Render to install the classic version of the tools to support legacy agents
try:
    import langchain
    import langchain_classic
except ModuleNotFoundError:
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", 
        "streamlit", "langchain", "langchain-classic", "langchain-groq", "langchain-community", "duckduckgo-search", "pypdf"
    ])

import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# --- FIX: IMPORT AGENT WRAPPERS FROM THE NATIVE CLASSIC DIRECTORY ---
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import Tool

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

def run_live_web_search(query: str) -> str:
    return web_search_engine.run(query)

def scan_local_data_files(query: str) -> str:
    try:
        loader = PyPDFDirectoryLoader("data/")
        docs = loader.load()
        if not docs:
            return "Local data folder is empty."
        return " ".join([d.page_content for d in docs if query.lower() in doc.page_content.lower()][:3])
    except:
        return "Could not read files."

tools = [
    Tool(name="search_the_live_web", func=run_live_web_search, description="Search live web data."),
    Tool(name="read_local_spiritual_library", func=scan_local_data_files, description="Read local data files.")
]

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
