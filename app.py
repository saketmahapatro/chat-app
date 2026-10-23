import streamlit as st
import json

# --- Crash-Proof Local Session Memory ---
# This initializes memory stored safely right inside your browser session
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- UI Layout Elements ---
st.title("💬 Pure Python Local Real-Time Chat")
st.caption("Self-Contained Local Memory Mode")

# 1. Reveal your profile options
user_name = st.sidebar.text_input("Enter your nickname:", value="Anonymous")

# 2. Render active message containers
chat_placeholder = st.container(height=400)
with chat_placeholder:
    for msg in st.session_state.messages:
        if msg["user"] == user_name:
            st.chat_message("user").write(f"**You:** {msg['text']}")
        else:
            st.chat_message("assistant").write(f"**{msg['user']}:** {msg['text']}")

# 3. Handle data injection on click/enter
if prompt := st.chat_input("Type your message here..."):
    # Append message directly to state logs
    st.session_state.messages.append({"user": user_name, "text": prompt})
    # Force a clean immediate UI paint refresh
    st.rerun()
