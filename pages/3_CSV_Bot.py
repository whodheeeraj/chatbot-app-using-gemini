import streamlit as st
import google.generativeai as genai
import pandas as pd

st.logo("https://dme2wmiz2suov.cloudfront.net/Institution(8663)/Logo/4216689-ThinkRook_Logo.png", size="large")

st.sidebar.title("Bot Settings")

with st.sidebar:
    
    model_name = st.selectbox(
        "Select Your Model",
        ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"],
        key="gemini_model"
    )
    gemini_api_key = st.text_input("Gemini API Key", key="gemini_api_key", type="password")


st.title("📝 CSV Bot with ThinkRook")
st.caption("Chat with your uploaded CSV file.")

uploaded_file = st.file_uploader("Upload your CSV here.", type=("csv"))

if not gemini_api_key:
    st.info("Please add your Google API key to continue.")
    st.stop()

genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel(model_name)

# Initializing the session state for chat
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.df = ""

# If a new file is uploaded, read and store the article/file
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.session_state.df = df
    csv_preview = st.session_state.df.head(50).to_string(index=False)

    if not any(msg["role"]=="assistant" for msg in st.session_state.messages):
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "CSV Uploaded! You can now ask me questions about it."
        })

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


if prompt := st.chat_input("Ask me something about the CSV file."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    chat_prompt = f"""
                        You are a data analyst. Use the following CSV data to answer my question.
                        CSV data: {csv_preview},
                        Question: {prompt}
    """

    chat = model.start_chat(history=[])
    response = chat.send_message(chat_prompt)

    st.session_state.messages.append({"role": "assistant", "content": response.text})
    st.chat_message("assistant").write(response.text)