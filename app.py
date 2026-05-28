import streamlit as st
import yt_dlp

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
            st.error(f"Gagal mengambil data video. Pastikan URL benar. Error: {e}")
            return None

def generate_advanced_prompt(title, user_instruction):
    """Menggabungkan judul video dengan instruksi custom dari user secara otomatis"""
    base_prompt = (
        f"Create a high-clickability YouTube thumbnail design inspired by the topic: '{title}'. "
        f"The style should be modern, vibrant, and eye-catching with high contrast and dynamic lighting. "
    )
    
    # Jika user menulis perintah tambahan, masukkan ke dalam prompt
    if user_instruction:
        base_prompt += f"Additional modification: {user_instruction}. "
        
    # Tambahan format standar AI untuk aspect ratio thumbnail youtube (16:9)
    base_prompt += "Cinematic composition, 4k resolution, optimized for YouTube aspect ratio --ar 16:9"
    return base_prompt

# --- INTERFAS PENGGUNA (UI) ---
st.title("📸 YT Thumbnail Downloader & Redesigner")
st.write("Unduh thumbnail YouTube dan buat *prompt* AI untuk mendesain ulang dengan mudah!")

# Input URL Video
video_url = st.text_input("Masukkan URL Video YouTube:", placeholder="
                          
