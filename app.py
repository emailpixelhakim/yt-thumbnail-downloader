import streamlit as st
import yt_dlp
import requests

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="YT Thumbnail Downloader & Redesigner", page_icon="📸", layout="centered")

def get_video_info(url):
    """Mengambil ID video, judul, dan thumbnail menggunakan yt-dlp"""
    ydl_opts = {'quiet': True, 'skip_download': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return {
                "id": info.get("id"),
                "title": info.get("title"),
                "thumbnail": info.get("thumbnail")
            }
        except Exception as e:
            return None

def generate_advanced_prompt(title, user_instruction):
    """Menggabungkan judul video dengan instruksi custom dari user secara otomatis"""
    base_prompt = (
        f"Create a high-clickability YouTube thumbnail design inspired by the topic: '{title}'. "
        f"The style should be modern, vibrant, and eye-catching with high contrast and dynamic lighting. "
    )
    if user_instruction:
        base_prompt += f"Additional modification: {user_instruction}. "
    base_prompt += "Cinematic composition, 4k resolution, optimized for YouTube aspect ratio --ar 16:9"
    return base_prompt

# --- INTERFAS PENGGUNA (UI) ---
st.title("📸 YT Thumbnail Downloader & Redesigner")
st.write("Unduh thumbnail YouTube dan buat *prompt* AI untuk mendesain ulang dengan mudah!")

# Inisialisasi session state untuk menyimpan teks paste
if "url_input" not in st.session_state:
    st.session_state.url_input = ""

# 1. Kolom URL dengan Tombol Tambahan
st.subheader("🔗 Tautan Video")
col_url, col_paste = st.columns([4, 1])

with col_url:
    video_url = st.text_input(
        "Masukkan URL Video YouTube:", 
        value=st.session_state.url_input,
        placeholder="https://www.youtube.com/watch?v=...",
        label_visibility="collapsed"
    )

with col_paste:
    # Tombol Paste menggunakan fitur bawaan browser (clipboard API) via trik HTML/JS Streamlit
    # Dikarenakan keterbatasan python server-side, kita buat tombol simulasi isi cepat jika sudah di-copy
    if st.button("📋 Paste", use_container_width=True):
        st.info("Silakan tahan kolom input lalu pilih 'Tempel/Paste' bawaan HP kamu.")

if video_url:
    with st.spinner("Mengambil data video..."):
        video_data = get_video_info(video_url)
    
    if video_data:
        video_id = video_data["id"]
        video_title = video_data["title"]
        
        st.success(f"Video Ditemukan: **{video_title}**")
        
        # Link Gambar Kualitas Tertinggi (HD)
        hd_thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        
        # Tampilkan Preview Thumbnail
        st.image(hd_thumbnail_url, caption="Preview Thumbnail Utama", use_container_width=True)
        
        # Fitur Auto-Download File Gambar HD (Langsung download tanpa buka tab baru)
        try:
            response = requests.get(hd_thumbnail_url)
            img_data = response.content
            
            # Tombol Download HD Otomatis tepat di bawah foto
            st.download_button(
                label="📥 Download Thumbnail (Kualitas HD)",
                data=img_data,
                file_name=f"thumbnail_{video_id}.jpg",
                mime="image/jpeg",
                use_container_width=True
            )
        except:
            st.warning("Gagal memproses tombol unduh otomatis. Gunakan alternatif klik kanan/tahan pada gambar lalu simpan.")

        st.markdown("---")
        
        # 2. Fitur Modifikasi dengan Tombol Create
        st.subheader("🎨 Modifikasi & Recreate Desain")
        st.write("Ketik perintah perubahan yang kamu inginkan di bawah ini:")
        
        col_cmd, col_btn = st.columns([4, 1])
        
        with col_cmd:
            custom_command = st.text_input(
                "Ketik perintah modifikasi di sini:", 
                placeholder="Contoh: buat background warna merah, tambah efek petir",
                label_visibility="collapsed"
            )
        
        # Inisialisasi trigger tombol klik
        if "start_create" not in st.session_state:
            st.session_state.start_create = False
            
        with col_btn:
            if st.button("🚀 Create", type="primary", use_container_width=True):
                st.session_state.start_create = True
        
        # Proses pembuatan prompt hanya jika tombol "Create" ditekan
        if st.session_state.start_create:
            final_prompt = generate_advanced_prompt(video_title, custom_command)
            
            st.markdown("**Hasil Prompt AI Siap Salin:**")
            
            # Menggunakan komponen st.code bawaan Streamlit yang secara OTOMATIS
            # memunculkan tombol "COPY" di pojok kanan atas kotaknya saat disentuh/diklik di HP!
            st.code(final_prompt, language="text")
            
            st.success("✅ Prompt berhasil dibuat! Klik ikon kotak bertumpuk di pojok kanan atas kolom abu-abu untuk COPY instan.")
