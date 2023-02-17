# Cohere's imports
import cohere as co
from cohere.classify import Example
from conversant.prompt_chatbot import PromptChatbot
from conversant.utils import demo_utils
from qa.bot import GroundedQaBot
from qa.search import get_results_paragraphs_multi_process

# Sreamlit
import streamlit as st
from streamlit_chat import message
import streamlit.components.v1 as components

# general imports
import os
import logging
import pandas as pd
import datetime
import random
from typing import Literal, Optional, Union

COHERE_API = "Qn83qLsfj9Bx3WiIWzzONJkz0gnIrW7xkmtn6KQX"
SERP_API = "9740e18bde5c0cb3e387237a3ccada2537c077a325253269207ac44e5724150e"

co = co.Client(COHERE_API)

#qa_bot = GroundedQaBot(COHERE_API, SERP_API)
health_e = PromptChatbot.from_persona("health-e", client=co)
qa_bot = GroundedQaBot(COHERE_API, SERP_API)

question = "What should I do about my finger cut?"

answer = qa_bot.answer(question)
print(answer)
        