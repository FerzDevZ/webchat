import streamlit as st
import json
import os
from datetime import datetime
import hashlib
import time

st.set_page_config(page_title="Web Chat Multi-User", page_icon="💬", layout="centered")
st.title("💬 Web Chat Multi-User")

CHAT_FILE = "chat_history.json"
REFRESH_INTERVAL = 5  # detik

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

# Fungsi avatar (emoji berdasarkan hash username)
def get_avatar(username):
    emojis = ['😀','😃','😄','😁','😆','😅','😂','🙂','🙃','😉','😊','😇','🥰','😍','🤩','😘','😗','😚','😙','😋','😜','🤪','🤨','🧐','🤓','😎','🥳','😏','😒','😞','😔','😟','😕','🙁','☹️','😣','😖','😫','😩','🥺','😢','😭','😤','😠','😡','🤬','🤯','😳','🥵','🥶','😱','😨','😰','😥','😓','🤗','🤔','🤭','🤫','🤥','😶','😐','😑','😬','🙄','😯','😦','😧','😮','😲','🥱','😴','🤤','😪','😵','🤐','🥴','🤢','🤮','🤧','😷','🤒','🤕','🤑','🤠','😈','👿','👹','👺','🤡','💩','👻','💀','☠️','👽','👾','🤖','🎃']
    idx = int(hashlib.sha256(username.encode()).hexdigest(), 16) % len(emojis)
    return emojis[idx]

# Fungsi warna bubble berdasarkan username
def get_bubble_color(username):
    colors = ["#DCF8C6", "#F1F0F0", "#E6E6FA", "#FFFACD", "#FFDAB9", "#E0FFFF", "#FFB6C1", "#D1FFD6", "#FFDEAD", "#C6E2FF"]
    idx = int(hashlib.sha256(username.encode()).hexdigest(), 16) % len(colors)
    return colors[idx]

# Login user
if "username" not in st.session_state:
    st.session_state["username"] = ""

if not st.session_state["username"]:
    st.session_state["username"] = st.text_input("Masukkan username Anda:", "")
    if st.session_state["username"]:
        st.rerun()
    st.stop()

# Auto refresh (polling)
st_autorefresh = st.empty()
if "last_refresh" not in st.session_state:
    st.session_state["last_refresh"] = time.time()
if time.time() - st.session_state["last_refresh"] > REFRESH_INTERVAL:
    st.session_state["last_refresh"] = time.time()
    st.rerun()
else:
    st_autorefresh.info(f"Auto refresh setiap {REFRESH_INTERVAL} detik. Terakhir: {datetime.now().strftime('%H:%M:%S')}")

# Load chat
messages = load_messages()

# Tampilkan riwayat chat
def render_chat():
    for msg in messages:
        align = 'right' if msg["user"] == st.session_state["username"] else 'left'
        bg = get_bubble_color(msg["user"])
        margin = "4px 0 4px 40px" if align == 'right' else "4px 40px 4px 0"
        sender = "Anda" if align == 'right' else msg["user"]
        avatar = get_avatar(msg["user"])
        st.markdown(f"<div style='display:flex; flex-direction:{'row-reverse' if align=='right' else 'row'}; align-items:flex-end; margin-bottom:2px;'><div style='font-size:28px; margin:0 8px;'>{avatar}</div><div style='text-align:{align}; background:{bg}; padding:10px 16px; border-radius:16px; margin:{margin}; min-width:80px; max-width:70%; box-shadow:0 1px 2px #ccc;'><b style='font-size:13px;'>{sender}</b><br><span style='font-size:15px;'>{msg['content']}</span><br><span style='font-size:10px;color:gray'>{msg['time']}</span></div></div>", unsafe_allow_html=True)

chat_placeholder = st.container()
with chat_placeholder:
    render_chat()

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

st.markdown("""
---
**Cara publish ke Streamlit Cloud:**
1. Push file ini dan `chat_history.json` (isi awal: `[]`) ke GitHub.
2. Buka [streamlit.io/cloud](https://streamlit.io/cloud) dan hubungkan ke repo Anda.
3. Pilih file `app.py` sebagai entry point.
4. Klik Deploy!
""")
