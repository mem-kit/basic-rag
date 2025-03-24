from dotenv import load_dotenv

import os, time, logging
import streamlit as st

from rag.rag_index_holder import RagIndexHolder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Initialize session objects
if "conversation_mode" not in st.session_state:
    st.session_state.conversation_mode = False

if "messages_rag" not in st.session_state:
    st.session_state.messages_rag = []

if "prompt" not in st.session_state:
    st.session_state.prompt = ''

if "input_disabled" not in st.session_state:
    st.session_state.input_disabled = False

with st.spinner('Initializing...'):
    print("Initializing...")
    st.session_state.conversation_mode = False

SSGenAIClient = os.getenv("RAI_SSGenAIClient")
SSGenAIAuth = os.getenv("RAI_SSGenAIAuth")
FAQ_BASE_INDEX_PATH = os.getenv("FAQ_BASE_INDEX_PATH")


def save_chat_history():
    with st.spinner('Submitting data into server...'):
        st.success("Chat history saved!")


def response_rag(question):
    with st.spinner('Analyzing with RAG API...'):
        if st.session_state.conversation_mode and len(st.session_state.messages_rag) > 0:
            history = []
            for m in st.session_state.messages_rag:
                history.append((m["role"], m["content"]))
            response = RagIndexHolder.conversation(history, question)
        else:
            response = RagIndexHolder.ask_question(question)

    if not isinstance(response, dict):
        response = response.dict()
    answer = response["answer"]
    logger.info(f"The answer is {answer}")
    for line in answer.splitlines(keepends=True):
        yield line
        time.sleep(0.05)


st.subheader("", divider="red")

with st.expander("ℹ️ Disclaimer:"):
    st.write(
        "This app is for testing purposes only. It connects to the Baidu QianWen API and monitors all traffics. "
        + "Please :red[DO NOT] leak sensitive or confidential information to this chat. "
          )

# Display chat messages from history on app rerun
for message in st.session_state.messages_rag:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if not st.session_state.input_disabled:
    prompt = st.chat_input("Please type your question here, thank you.")
    # Accept user input
    if prompt:
        st.markdown("""
        <style>
         textarea {pointer-events: none;display: none;}
        </style>
        """, unsafe_allow_html=True)

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.input_disabled = True

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = st.write_stream(
                response_rag(
                    question=prompt
                )
            )
        ##
        # Add user message to chat history
        st.session_state.messages_rag.append({"role": "user", "content": prompt})
        # Add assistant response to chat history
        st.session_state.messages_rag.append({"role": "assistant", "content": response})
        st.session_state.input_disabled = False
        st.markdown("""
        <style>
         textarea {pointer-events: auto;display: block;}
        </style>
        """, unsafe_allow_html=True)
        if st.button("Submit Chat History to Admin"):
            save_chat_history()
else:
    st.chat_input("Please type your question here, thank you.")
    st.markdown("""
    <style>
     textarea {pointer-events: auto;display: block;}
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    for it in range(0, 15):
        st.write("\n")
    st.markdown("---")

mode = st.sidebar.toggle("Conversation Mode", value=st.session_state.conversation_mode, key="use_conversation_mode")
if mode != st.session_state.conversation_mode:
    st.session_state.conversation_mode = mode
    st.rerun(scope="app")
##
if st.session_state.messages_rag:
    reset = st.sidebar.button("Start New Conversation")
    if reset:
        logger.info("reset")
        st.session_state.messages_rag = []
        st.rerun(scope="app")
