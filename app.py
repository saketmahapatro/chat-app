import streamlit as st
import paho.mqtt.client as mqtt
import json
import uuid

# --- Shared Global Live Network Configuration ---
# Uses a free public broker to route messages between different computers instantly
MQTT_BROKER = "://hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "saket_global_chat_room_2026"

# Give this specific browser tab a unique ID
if "user_uuid" not in st.session_state:
    st.session_state.user_uuid = str(uuid.uuid4())

# Initialize shared message memory list
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Background Network Event Handler ---
def on_message(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode())
        # Avoid duplication loops from our own broadcast outputs
        if payload.get("sender_id") != st.session_state.user_uuid:
            st.session_state.messages.append(payload)
            st.rerun()
    except Exception:
        pass

# Maintain a persistent network client instance across UI hot-reloads
if "mqtt_client" not in st.session_state:
    client = mqtt.Client()
    client.on_message = on_message
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.subscribe(MQTT_TOPIC)
        client.loop_start()
        st.session_state.mqtt_client = client
    except Exception:
        st.error("Connection to global chat network failed. Retrying...")

# --- UI Layout Elements ---
st.title("💬 Live Shared Friends Chat App")
st.caption("Connected to Global Real-Time Network Router")

# 1. Nickname configuration
user_name = st.sidebar.text_input("Enter your nickname:", value="Anonymous User")

# 2. Render active message containers
chat_placeholder = st.container(height=400)
with chat_placeholder:
    for msg in st.session_state.messages:
        if msg["sender_id"] == st.session_state.user_uuid:
            st.chat_message("user").write(f"**You:** {msg['text']}")
        else:
            st.chat_message("assistant").write(f"**{msg['user']}:** {msg['text']}")

# 3. Handle message transmission to friends
if prompt := st.chat_input("Type your message here..."):
    msg_data = {
        "user": user_name,
        "text": prompt,
        "sender_id": st.session_state.user_uuid
    }
    # Append locally instantly
    st.session_state.messages.append(msg_data)
    
    # Broadcast to all listening friends globally
    if "mqtt_client" in st.session_state:
        st.session_state.mqtt_client.publish(MQTT_TOPIC, json.dumps(msg_data))
    
    st.rerun()
    
