import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from streamlit_chat import message
from backend.llm import LLM, StreamHandler
from backend.vectorstore import load_vector_store
from backend.config import config
import uuid

st.set_page_config(
    page_title="Klaipėdos uosto rinkliavos asistentas",
    page_icon="🚢"
)
st.title("Klaipėdos uosto rinkliavos asistentas")

# Initialize session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'session_id' not in st.session_state:
    st.session_state['session_id'] = str(uuid.uuid4())
if 'chatbot' not in st.session_state:
    index_name = 'seaport-chatbot'
    vector_store = load_vector_store(index_name)
    st.session_state['chatbot'] = LLM(vector_store)

# User input
user_input = st.text_input("You:", key="user_input")

if user_input:
    st.session_state.past.append(user_input)

    message(user_input, is_user=True, key=f"{len(st.session_state.past)}_user")

    stream_container = st.empty()
    stream_handler = StreamHandler(stream_container)

    output = st.session_state['chatbot'].ask(
        user_input,
        st.session_state['session_id'],
        stream_handler
    )

    st.session_state.generated.append(output)

st.empty()