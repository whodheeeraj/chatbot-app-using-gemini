# Step : 1 > Install Google SDK
# Step : 2 > Import Google SDK
# Step : 3 > Write a message on the screen
# Step : 4 > Added Navbar
# Step : 5 > Grant the user the ability to add their gemini api key and choose the model.

import streamlit as st
import google.generativeai as genai

st.logo("https://dme2wmiz2suov.cloudfront.net/Institution(8663)/Logo/4216689-ThinkRook_Logo.png", size="large")

st.sidebar.title("Bot Settings")

with st.sidebar:
    
    model = st.selectbox(
        "Select Your Model",
        ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"],
        key="gemini_model"
    )

    gemini_api_key = st.text_input("Gemini API Key", key="gemini_api_key", type="password")


st.title("ThinkRook Gemini Bot")
st.caption("Hello from Gemini Bot by ThinkRook.")

# api_key = "your-api-key"
# model_name ="gemini-2.5-flash"

# genai.configure(api_key=api_key)
# model = genai.GenerativeModel(model_name)

if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    if not gemini_api_key:
        st.info("Please add your Google API key to continue.")
        st.stop()
    
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel(model)

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    chat = model.start_chat(history=[])
    response = chat.send_message(prompt)

    st.session_state.messages.append({"role": "assistant", "content": response.text})
    st.chat_message("assistant").write(response.text)
