import streamlit as st
import requests


# FastAPI endpoints
UPLOAD_URL = "http://127.0.0.1:8000/upload/"
CHAT_URL = "http://127.0.0.1:8000/chat/"

# Streamlit UI
st.set_page_config(page_title="AI PDF Chatbot", layout="wide")

st.title("📄 AI PDF Chatbot 🤖")
st.sidebar.header("Upload PDF Documents")

# File uploader
uploaded_file = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Uploading and processing PDF..."):
        files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        response = requests.post(UPLOAD_URL, files=files)

    if response.status_code == 200:
        st.sidebar.success("PDF uploaded and indexed successfully!")
    else:
        st.sidebar.error(f"Error: {response.json()['detail']}")

# Chat UI
st.subheader("💬 Chat with Your PDF")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Ask a question about the uploaded PDFs...")

if user_input:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send request to chatbot API
    with st.spinner("Thinking..."):
        response = requests.post(CHAT_URL, json={"question": user_input})

    if response.status_code == 200:
        bot_reply = response.json()["answer"]
    else:
        bot_reply = "Error: Unable to fetch response."

    # Display chatbot response
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
