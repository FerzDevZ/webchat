# Web Chat Multi-User 🚀💬

[![Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/FerzDevZ/webchat)
[![GitHub stars](https://img.shields.io/github/stars/FerzDevZ/webchat?style=social)](https://github.com/FerzDevZ/webchat)
[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Aplikasi web chat multi-user modern berbasis **Python** & **Streamlit**. Login dengan username, pilih avatar emoji, dan nikmati chat real-time (auto-refresh) dengan tampilan bubble chat stylish, dark mode, notifikasi pesan baru, dan fitur interaktif lain! 🚀

---

## ✨ Fitur Utama

- 🗨️ **Multi-user chat:** Semua user bisa saling berkirim pesan secara langsung.
- 👤 **Login username:** Masuk dengan username unik, tanpa password.
- 😎 **Avatar emoji custom:** Pilih emoji favorit sebagai avatar di sidebar.
- 💬 **Bubble chat modern:** Tampilan chat mirip WhatsApp/Telegram, warna bubble otomatis.
- 🌙 **Dark mode:** Ganti tema gelap/terang dengan satu klik.
- 🔔 **Notifikasi pesan baru:** Sidebar menampilkan badge jika ada pesan baru.
- 🕒 **Waktu informatif:** Tanggal/waktu otomatis ("Hari ini", "Kemarin", dst).
- 🔄 **Auto refresh:** Chat update otomatis tiap 2 detik.
- 🔓 **Logout/ganti username:** Bisa logout & ganti avatar kapan saja.

---

## 🚀 Demo Langsung

Klik badge di atas atau buka: [webchat di Streamlit Cloud](https://share.streamlit.io/FerzDevZ/webchat)

---

## 🛠️ Cara Menjalankan Lokal

1. **Clone repo:**
   ```bash
   git clone https://github.com/FerzDevZ/webchat.git
   cd webchat
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Jalankan aplikasi:**
   ```bash
   streamlit run app.py
   ```
4. **Akses di browser:**
   Buka [http://localhost:8501](http://localhost:8501)

---

## ☁️ Cara Deploy ke Streamlit Cloud

1. **Push file berikut ke GitHub:**
   - `app.py`
   - `chat_history.json` (isi awal: `[]`)
   - `requirements.txt`
2. **Buka [streamlit.io/cloud](https://streamlit.io/cloud)**
3. **Hubungkan ke repo GitHub Anda**
4. **Pilih file `app.py` sebagai entry point**
5. **Klik Deploy!**

---

## 📁 Struktur File

```
webchat/
├── app.py                # Main Streamlit app
├── chat_history.json     # File penyimpanan riwayat chat (format JSON)
├── requirements.txt      # Daftar dependensi Python
└── .devcontainer/        # (Opsional) Konfigurasi devcontainer
```

---

## 🧩 Penjelasan Fitur & Kode

<details>
<summary><b>Penyimpanan Chat</b></summary>
Semua pesan disimpan di file <code>chat_history.json</code> (format list of dict JSON). Setiap pesan berisi: username, isi pesan, waktu kirim.
</details>

<details>
<summary><b>Avatar Emoji</b></summary>
User memilih avatar emoji di sidebar saat login. Avatar tampil di samping setiap pesan user.
</details>

<details>
<summary><b>Bubble Chat</b></summary>
Warna bubble chat otomatis berbeda untuk setiap user (berbasis hash username). Bubble chat rounded, modern, dan responsif.
</details>

<details>
<summary><b>Dark Mode</b></summary>
Dark mode di sidebar, mengubah warna background & teks.
</details>

<details>
<summary><b>Notifikasi Pesan Baru</b></summary>
Jika ada pesan baru (jumlah pesan bertambah), sidebar tampilkan badge notifikasi.
</details>

<details>
<summary><b>Auto Refresh</b></summary>
Chat otomatis refresh tiap 2 detik (polling).
</details>

<details>
<summary><b>Logout/Ganti Username</b></summary>
Tombol di sidebar untuk logout & memilih username/avatar baru.
</details>

---

## ⚠️ Keterbatasan

- ⏳ **Tidak real-time 100%:** Chat auto-refresh tiap 2 detik (polling), bukan WebSocket.
- 📄 **Penyimpanan file:** Semua pesan di satu file JSON. Jika banyak user mengirim bersamaan, ada risiko pesan hilang (race condition).
- 🚫 **Tidak ada upload file/gambar:** Fitur upload file/gambar & emoji picker di-nonaktifkan agar stabil di Streamlit Cloud.
- 🏠 **Tidak ada multi-room:** Semua user chat di satu ruang bersama.

---

## 💡 Saran Pengembangan Lanjutan

- 🏘️ Multi-room/group chat
- 🧹 Fitur clear chat (admin/user)
- 🔍 Pencarian pesan
- 📤 Export chat ke file
- 🏷️ Mention user (@username)
- 👥 User list online
- 📌 Pin/highlight pesan
- 🗄️ Integrasi database (Supabase/Firebase) untuk chat lebih aman & real-time

---

## 🤝 Kontribusi

Pull request & ide baru sangat diterima! Baca [CONTRIBUTING.md](CONTRIBUTING.md) jika ingin berkontribusi.

---

## 📜 Lisensi

MIT License © [FerzDevZ](https://github.com/FerzDevZ)
