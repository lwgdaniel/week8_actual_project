
##########  setup llm pipe
import streamlit as st
import openai 
import dotenv
import os
from dotenv import load_dotenv
from openai import OpenAI

#for local
#
# load_dotenv('.env')


keyyy = st.secrets["OPENAI_API_KEY"]

client = OpenAI(api_key=keyyy)

def get_completion_by_messages(messages, model="gpt-4o-mini", temperature=0, top_p=1.0, max_tokens=1024, n=1):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        n=1
    )
    return response.choices[0].message.content

# Check password

from utilities import check_password  

if not check_password():  
    st.stop()

# Streamlit App Configuration
st.set_page_config(layout="centered", page_title="CrapGPT")

st.title("a worse version of chatgpt version 2 for annabel")


# Sidebar for page navigation
page = st.sidebar.radio("Navigate", ["Chat", "About Us"])

if page == "Chat":

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display past messages
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    # Chat input 
    user_prompt = st.text_area("Write some text below...", height=100)

    # Add a submit button
    submit = st.button("Submit")

    if submit or user_prompt.strip():
        # Store user message
        st.session_state.messages.append({"role": "user", "content": user_prompt})

        # Generate model response
        response = get_completion_by_messages(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)

    print(st.session_state.messages)

elif page == "About Us":
    st.title("About Us")
    st.write("""
    Welcome to **CrapGPT**, the intentionally worse version of ChatGPT.  

    Our mission is to make AI conversations a bit more chaotic and humorous.  
    This project is purely for entertainment and experimentation purposes.
    """)

#Button to reset the app and clear session

if st.sidebar.button("Clear memory and reset"):
    st.session_state.clear()
    st.rerun()