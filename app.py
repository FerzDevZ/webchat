import streamlit as st
import json
import os
from datetime import datetime, timedelta
import hashlib
import time
import base64

st.set_page_config(page_title="Web Chat Multi-User", page_icon="💬", layout="centered")
st.title("💬 Web Chat Multi-User")

CHAT_FILE = "chat_history.json"
REFRESH_INTERVAL = 2  # detik

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

# Avatar custom (pilih emoji/avatar dari list)
def avatar_picker():
    emojis = ['😀','😃','😄','😁','😆','😅','😂','🙂','🙃','😉','😊','😇','🥰','😍','🤩','😘','😗','😚','😙','😋','😜','🤪','🤨','🧐','🤓','😎','🥳','😏','😒','😞','😔','😟','😕','🙁','☹️','😣','😖','😫','😩','🥺','😢','😭','😤','😠','😡','🤬','🤯','😳','🥵','🥶','😱','😨','😰','😥','😓','🤗','🤔','🤭','🤫','🤥','😶','😐','😑','😬','🙄','😯','😦','😧','😮','😲','🥱','😴','🤤','😪','😵','🤐','🥴','🤢','🤮','🤧','😷','🤒','🤕','🤑','🤠','😈','👿','👹','👺','🤡','💩','👻','💀','☠️','👽','👾','🤖','🎃']
    st.write("Pilih avatar emoji:")
    cols = st.columns(8)
    for i, emoji in enumerate(emojis):
        if cols[i % 8].button(emoji, key=f'avatar_{i}'):
            st.session_state['custom_avatar'] = emoji
            st.session_state['avatar_set'] = True
            st.rerun()

# Fungsi avatar (emoji berdasarkan custom user)
def get_avatar(username):
    if username == st.session_state.get("username") and st.session_state.get('avatar_set', False):
        return st.session_state['custom_avatar']
    # fallback: hash
    emojis = ['😀','😃','😄','😁','😆','😅','😂','🙂','🙃','😉','😊','😇','🥰','😍','🤩','😘','😗','😚','😙','😋','😜','🤪','🤨','🧐','🤓','😎','🥳','😏','😒','😞','😔','😟','😕','🙁','☹️','😣','😖','😫','😩','🥺','😢','😭','😤','😠','😡','🤬','🤯','😳','🥵','🥶','😱','😨','😰','😥','😓','🤗','🤔','🤭','🤫','🤥','😶','😐','😑','😬','🙄','😯','😦','😧','😮','😲','🥱','😴','🤤','😪','😵','🤐','🥴','🤢','🤮','🤧','😷','🤒','🤕','🤑','🤠','😈','👿','👹','👺','🤡','💩','👻','💀','☠️','👽','👾','🤖','🎃']
    idx = int(hashlib.sha256(username.encode()).hexdigest(), 16) % len(emojis)
    return emojis[idx]

# Fungsi warna bubble berdasarkan username
def get_bubble_color(username):
    gradients = [
        "linear-gradient(135deg, #DCF8C6 0%, #b2f7cc 100%)",
        "linear-gradient(135deg, #F1F0F0 0%, #e0e0e0 100%)",
        "linear-gradient(135deg, #E6E6FA 0%, #b8b8ff 100%)",
        "linear-gradient(135deg, #FFFACD 0%, #ffe29a 100%)",
        "linear-gradient(135deg, #FFDAB9 0%, #ffcba4 100%)",
        "linear-gradient(135deg, #E0FFFF 0%, #b2f7f7 100%)",
        "linear-gradient(135deg, #FFB6C1 0%, #ff8fab 100%)",
        "linear-gradient(135deg, #D1FFD6 0%, #a3ffb0 100%)",
        "linear-gradient(135deg, #FFDEAD 0%, #ffd180 100%)",
        "linear-gradient(135deg, #C6E2FF 0%, #a0c4ff 100%)"
    ]
    idx = int(hashlib.sha256(username.encode()).hexdigest(), 16) % len(gradients)
    return gradients[idx]

# Fungsi waktu informatif
def format_time(ts):
    now = datetime.now()
    try:
        t = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
    except:
        return ts
    if t.date() == now.date():
        return f"Hari ini, {t.strftime('%H:%M')}"
    elif t.date() == (now - timedelta(days=1)).date():
        return f"Kemarin, {t.strftime('%H:%M')}"
    else:
        return t.strftime('%d %b %Y, %H:%M')

# Sidebar: Avatar custom
with st.sidebar:
    st.header("Pengaturan")
    if st.button("Logout/Ganti Username"):
        st.session_state["username"] = ""
        st.session_state['avatar_set'] = False
        st.rerun()
    dark_mode = st.checkbox("Dark Mode", value=False)
    if not st.session_state.get('avatar_set', False):
        avatar_picker()
        st.stop()
    else:
        st.write(f"Avatar Anda: {st.session_state['custom_avatar']}")

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

# Notifikasi pesan baru (highlight badge jika ada pesan baru dan user tidak scroll ke bawah)
# Catatan: Streamlit tidak bisa deteksi posisi scroll browser secara native,
# jadi notifikasi hanya muncul jika jumlah pesan bertambah saat auto-refresh.
if 'last_message_count' not in st.session_state:
    st.session_state['last_message_count'] = len(messages)
if len(messages) > st.session_state['last_message_count']:
    st.sidebar.markdown('<span style="color:orange;font-weight:bold;">🔔 Ada pesan baru!</span>', unsafe_allow_html=True)
    st.session_state['last_message_count'] = len(messages)

# Tampilkan riwayat chat
def render_chat():
    for msg in messages:
        align = 'right' if msg["user"] == st.session_state["username"] else 'left'
        bg = get_bubble_color(msg["user"])
        margin = "4px 0 4px 40px" if align == 'right' else "4px 40px 4px 0"
        sender = "Anda" if align == 'right' else msg["user"]
        avatar = get_avatar(msg["user"])
        time_str = format_time(msg["time"])
        st.markdown(f"<div style='display:flex; flex-direction:{'row-reverse' if align=='right' else 'row'}; align-items:flex-end; margin-bottom:2px;'><div style='font-size:28px; margin:0 8px;'>{avatar}</div><div style='text-align:{align}; background:{bg}; padding:12px 18px; border-radius:22px; margin:{margin}; min-width:80px; max-width:70%; box-shadow:0 2px 8px #bbb; font-family:sans-serif;'><b style='font-size:13px;'>{sender}</b><br><span style='font-size:15px;'>{msg['content']}</span><br><span style='font-size:11px;color:gray'>{time_str}</span></div></div>", unsafe_allow_html=True)

# Dark mode CSS
if dark_mode:
    st.markdown("""
        <style>
        body, .stApp { background: #222 !important; color: #eee !important; }
        .stTextInput>div>div>input { background: #333 !important; color: #eee !important; }
        .stButton>button { background: #444 !important; color: #eee !important; }
        </style>
    """, unsafe_allow_html=True)

chat_placeholder = st.container()
with chat_placeholder:
    render_chat()

# Hapus fitur emoji picker dan upload file, gunakan input pesan sederhana
user_input = st.text_input("Ketik pesan Anda", key="chat_input_simple")
with st.form(key="chat_form", clear_on_submit=True):
    submit = st.form_submit_button("Kirim")

if submit and user_input.strip():
    messages = load_messages()
    new_msg = {
        "user": st.session_state["username"],
        "content": user_input,
        "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    messages.append(new_msg)
    save_messages(messages)
    st.session_state['chat_input_simple'] = ''
    st.rerun()

st.markdown("""
---
**Cara publish ke Streamlit Cloud:**
1. Push file ini dan `chat_history.json` (isi awal: `[]`) ke GitHub.
2. Buka [streamlit.io/cloud](https://streamlit.io/cloud) dan hubungkan ke repo Anda.
3. Pilih file `app.py` sebagai entry point.
4. Klik Deploy!
""")
