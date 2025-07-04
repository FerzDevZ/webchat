import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="Web Chat Multi-User", page_icon="💬", layout="centered")
st.title("💬 Web Chat Multi-User")

CHAT_FILE = "chat_history.json"

# Fungsi untuk load dan save chat

def load_messages():
    if not os.path.exists(CHAT_FILE):
        return []
    with open(CHAT_FILE, "r") as f:
        try:
            return json.load(f)
        except Exception:
            return []

def save_messages(messages):
    with open(CHAT_FILE, "w") as f:
        json.dump(messages, f)

# Login user
if "username" not in st.session_state:
    st.session_state["username"] = ""

if not st.session_state["username"]:
    st.session_state["username"] = st.text_input("Masukkan username Anda:", "")
    if st.session_state["username"]:
        st.rerun()
    st.stop()

# Load chat
messages = load_messages()

# Tampilkan riwayat chat
chat_placeholder = st.container()
with chat_placeholder:
    for msg in messages:
        align = 'right' if msg["user"] == st.session_state["username"] else 'left'
        bg = '#DCF8C6' if align == 'right' else '#F1F0F0'
        margin = "4px 0 4px 40px" if align == 'right' else "4px 40px 4px 0"
        sender = "Anda" if align == 'right' else msg["user"]
        st.markdown(f"<div style='text-align:{align}; background:{bg}; padding:8px; border-radius:10px; margin:{margin};'><b>{sender}:</b> {msg['content']}<br><span style='font-size:10px;color:gray'>{msg['time']}</span></div>", unsafe_allow_html=True)

# Input pesan
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Ketik pesan Anda", "")
    submit = st.form_submit_button("Kirim")

if submit and user_input.strip():
    new_msg = {
        "user": st.session_state["username"],
        "content": user_input,
        "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    messages.append(new_msg)
    save_messages(messages)
    st.rerun()

# Tombol refresh
if st.button("🔄 Refresh Chat"):
    st.rerun()

st.markdown("""
---
**Cara publish ke Streamlit Cloud:**
1. Push file ini dan `chat_history.json` (isi awal: `[]`) ke GitHub.
2. Buka [streamlit.io/cloud](https://streamlit.io/cloud) dan hubungkan ke repo Anda.
3. Pilih file `app.py` sebagai entry point.
4. Klik Deploy!
""")
