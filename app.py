import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Initialize client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Page config
st.set_page_config(page_title="AWS Cheat Code Bot", page_icon="☁️")

st.title("☁️ AWS Cheat Code Chatbot")
st.caption("Ask anything about AWS — get step-by-step solutions")

# Session state for chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
prompt = st.chat_input("Ask anything about AWS...")

if prompt:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # System prompt (AWS expert mode)
    system_prompt = """
    You are an AWS expert assistant.

    Always:
    - Give step-by-step instructions
    - Use simple explanations
    - Include AWS Console navigation steps
    - Include CLI commands if useful
    - Be concise but practical

    Focus on real-world implementation.
    """

    with st.chat_message("assistant"):
        response_text = ""
        message_placeholder = st.empty()

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                *st.session_state.messages
            ],
            temperature=0.7,
            max_tokens=1024,
            stream=True
        )

        for chunk in completion:
            content = chunk.choices[0].delta.content
            if content:
                response_text += content
                message_placeholder.markdown(response_text)

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": response_text}
    )
