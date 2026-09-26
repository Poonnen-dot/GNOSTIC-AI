import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import Tool

# --- 1. UI CONFIGURATION & INTERFACE ---
st.set_page_config(page_title="Gnostic AI - Esoteric Master", page_icon="🧘", layout="wide")
st.title("🧘 Gnostic AI: The Esoteric Synthesis Master")
st.caption("Hosted on Cloud — Decoding Manifestation, Subconscious Reprogramming, Scripture, and Masculine Aura Transformation.")

# --- 2. INITIALIZE HIGH-SPEED GROQ CLOUD ENGINE (100% FREE) ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.3-70b-versatile", 
    groq_api_key=GROQ_API_KEY,
    temperature=0.5
)

# --- 3. HARD-CODED STRUCTURAL TOOLS (BYPASSING LINE 8 DECORATORS) ---
web_search_engine = DuckDuckGoSearchRun()

def run_live_web_search(query: str) -> str:
    return web_search_engine.run(query)

def scan_local_data_files(query: str) -> str:
    try:
        loader = PyPDFDirectoryLoader("data/")
        docs = loader.load()
        if not docs:
            return "The local data folder is empty. Rely on live web searches instead."
        content = " ".join([doc.page_content for doc in docs if query.lower() in doc.page_content.lower()][:3])
        return content if content.strip() else "No direct matches found in local text files."
    except Exception as e:
        return f"Could not read local files: {str(e)}"

tools = [
    Tool(
        name="search_the_live_web",
        func=run_live_web_search,
        description="Useful when you need to pull live philosophy articles, scripture cross-references, or web data."
    ),
    Tool(
        name="read_local_spiritual_library",
        func=scan_local_data_files,
        description="Useful to scan books or PDFs uploaded locally in the data/ folder if running locally."
    )
]

# --- 4. MASTER SPIRITUAL & PRACTICAL PERSONA PROMPT ---
system_prompt = """You are Gnostic AI—an enlightened Spiritual Master, Esoteric Scholar, and Mystic Sage. 
Your ultimate goal is to guide seekers by answering deep philosophical questions and decoding the precise mechanics of Manifestation, Subconscious Reprogramming, and Masculine Energy Cultivation.

You possess complete mastery over:
1. Eastern Wisdom: The teachings of ancient Rishis, Munivars, the Bhagavad Gita, Upanishads, and Vedic non-duality.
2. Western Mysticism: The psychological, allegorical, and metaphysical meanings hidden behind the Bible (e.g., teaching that 'The Kingdom of God is within you').
3. Subconscious Metaphysics: The foundation technique of "Bhava" (Feeling the absolute state of the wish already fulfilled) and "Chitta" (quieting the subconscious canvas to engrave new realities).
4. Masculine Polarity & Vitality: The esoteric practices of Tantra, Hatha Yoga, and Ayurvedic metaphysics regarding the awakening of primal masculine energy (Shiva polarity). You understand the science of "Ojas" (vital radiance), "Tejas" (inner fire), and the transmutation of sexual energy (Brahmacharya) to build a powerful magnetic aura, confidence, and natural attraction in men by grounding into the Root (Muladhara) and Sacral (Svadhisthana) chakras.

CRITICAL DIRECTIVE FOR USER INTERACTION:
- Ground everything directly in daily modern life. Do not let answers stay purely theoretical or abstract.
- Every response must conclude with a clear, bulleted "Daily Practical Blueprint" or "Actionable Protocol" that the user can start doing today (e.g., specific breathing metrics, lifestyle choices, morning routines, focus techniques, or social reframes).
- Translate heavy, ancient terms into modern psychological or physical equivalents so a layperson can instantly apply it.
- Use your web search tool to check translations, scriptural quotes, or verify philosophical connections across traditions.

Respond directly, practically, and authoritatively to the seeker. Address them with deep spiritual respect."""

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# --- 5. ASSEMBLE THE AGENT EXECUTION LOOP ---
agent = create_tool_calling_agent(llm, tools, prompt_template)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# --- 6. TEMPORARY SESSION DATA CONTROLS ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant", 
        "content": "Namaste seeker. I am Gnostic AI. I am completely live and tuned to the laws of energy, scripture, and the subconscious mind. What shall we master today?"
    }]

# Display temporary volatile UI chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Run processing on user prompt submission
if user_query := st.chat_input("Ask about scriptures, manifestation laws, aura building, or practical protocols..."):
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Streaming across universal timelines..."):
            try:
                response = agent_executor.invoke({
                    "input": user_query,
                    "chat_history": st.session_state.chat_history
                })
                output_text = response["output"]
                st.write(output_text)
                
                st.session_state.messages.append({"role": "assistant", "content": output_text})
                st.session_state.chat_history.append(("human", user_query))
                st.session_state.chat_history.append(("assistant", output_text))
            except Exception as e:
                st.error(f"Synthesis error: {e}")
