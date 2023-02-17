import re
import os
import logging
import pandas as pd
import datetime
import random
from typing import Literal, Optional, Union

import cohere as co
from conversant.prompt_chatbot import PromptChatbot
from qa.bot import GroundedQaBot

import streamlit as st
import streamlit.components.v1 as components


#------------------------------------------------------------
COMPONENT_NAME = "streamlit_chat"

# data type for avatar style
AvatarStyle = Literal[ 
    "adventurer", 
    "adventurer-neutral", 
    "avataaars",
    "big-ears",
    "big-ears-neutral",
    "big-smile",
    "bottts", 
    "croodles",
    "croodles-neutral",
    "female",
    "gridy",
    "human",
    "identicon",
    "initials",
    "jdenticon",
    "male",
    "micah",
    "miniavs",
    "pixel-art",
    "pixel-art-neutral",
    "personas",
]

root_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(root_dir, "pages/frontend/build")

_streamlit_chat = components.declare_component(
    COMPONENT_NAME,
    path = build_dir)

# -----------------------------------------------------------

def is_question(text):
    question_words = ["what", "when", "where", "who", "why", "how", "which", "?"]
    question_regex = "|".join(question_words)
    if re.search(f"^{question_regex}", text, re.IGNORECASE):
        return True
    else:
        return False

@st.cache(allow_output_mutation=True, show_spinner=True)
def query_bot(COHERE_API,
              SERP_API,
              text_input: str,
              qa: bool):
    
    co = co.Client(COHERE_API)
    
    if qa:
        bot = GroundedQaBot(COHERE_API, SERP_API)
        output = bot.answer(text_input)

    else:
        health_e = PromptChatbot.from_persona("health-e", client=co)
        output = health_e.reply(text_input)

    return output

def get_text():
    input_text = st.text_input("Hello! How may I assist you?", "", key="input_text")
    return input_text 

def chat_message_ui(message: str,
                    is_user: bool = False, # choose random string from AvatarStyle for default
                    avatar_style: Optional[AvatarStyle] = None,
                    seed: Optional[Union[int, str]] = 42,
                    key: Optional[str] = None):
    '''
    Streamlit chat frontend style and display
    '''
    if not avatar_style:
        avatar_style = "pixel-art-neutral" if is_user else "bottts"

    _streamlit_chat(message=message, seed=seed, isUser=is_user, avatarStyle=avatar_style, key=key)
    
def init_chat():
    '''
    Initialize all session states. 
    Streamlit requires unique keys per session state. 
    Keep all states separated and independent from each other to avoid multiprocessing issues.
    '''
    if ('patient_description' not in st.session_state):
        st.session_state['patient_description'] = []
    
    if ('healthE_output' not in st.session_state):
        st.session_state['healthE_output'] = []
        
    if ('patient_question' not in st.session_state):
        st.session_state['patient_question'] = []    
    
    if ("QA_output" not in st.session_state):
        st.session_state['QA_output'] = []
        
    if ("history_outputs" not in st.session_state):
        st.session_state['history_outputs'] = []
        
    if ("history_inputs" not in st.session_state):
        st.session_state['history_inputs'] = []
        
    if ("random_id" not in st.session_state):
        st.session_state['random_id'] = random.randint(0, 1000)
        
    if ("session_report" not in st.session_state):
        st.session_state['session_report'] = []

    logging.info(st.session_state.keys)