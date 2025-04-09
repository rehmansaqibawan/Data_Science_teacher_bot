import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os

# Set up API key
os.environ["GROQ_API_KEY"] = "gsk_2zTFCQ0KaRwlmXygo7vHWGdyb3FYjAmTXY7KPHkH6dvr7u5aHoN"

# Page title
st.title('Data Science Teacher!')

# Session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])

# User input
prompt = st.chat_input('Pass your prompt here')

# Only run the chatbot logic if there is a prompt
if prompt:
    # Show user message
    st.chat_message('user').markdown(prompt)
    st.session_state.messages.append({'role': 'user', 'content': prompt})

    # Set up system prompt
    groq_sys_prompt = ChatPromptTemplate.from_template("""
    You are an expert data science teacher. You deeply understand all the topics and can explain them very well:
    {user_prompt}.
    Start the answer directly. No small talk please.3 lines answers.
    """)

    # Initialize Groq Chat with correct args
    groq_chat = ChatGroq(
        api_key=os.environ.get("GROQ_API_KEY"),
        model="llama-3.3-70b-versatile"  # or another valid model
    )

    # Chain: prompt → model → output
    chain = groq_sys_prompt | groq_chat | StrOutputParser()

    # Run chain with user input
    response = chain.invoke({"user_prompt": prompt})

    # Show assistant response
    st.chat_message('assistant').markdown(response)
    st.session_state.messages.append({'role': 'assistant', 'content': response})
