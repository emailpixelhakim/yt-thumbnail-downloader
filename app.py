import streamlit as tf
import re
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

def generate_redesign_prompt(title):
    """Membuat prompt otomatis untuk recreate/redesign thumbnail berdasarkan judul"""
    prompt = (
        f"Create a high-clickability YouTube thumbnail design inspired by the topic: '{title}'. "
        f"The style should be modern, vibrant, and eye-catching with high contrast, bold typography placeholders, "
        f"and dynamic lighting. Cinematic composition, 4k resolution, optimized for YouTube 16:9 aspect ratio --ar 16:9"
    )
    return prompt

# --- INTERFAS PENGGUNA (UI) ---
st.title("📸 YT Thumbnail Downloader & Redesigner")
st.write("Unduh thumbnail YouTube dan dapatkan *prompt* otomatis untuk mendesain ulang menggunakan AI!")

# Input URL Video
video_url = st.text_input("Masukkan URL Video YouTube:", placeholder="https://www.youtube.com/watch?v=...")

if video_url:
    with st.spinner("Mengambil data video..."):
        video_data = get_video_info(video_url)
    
    if video_data:
        video_id = video_data["id"]
        video_title = video_data["title"]
        
        st.success(f"Video Ditemukan: **{video_title}**")
        
        # Variasi resolusi thumbnail YouTube
        resolutions = {
            "Max Res (HD - 1080p/720p)": f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
            "High Quality (480p)": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
            "Medium Quality (360p)": f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg",
            "Standard Quality (240p)": f"https://img.youtube.com/vi/{video_id}/default.jpg"
        }
        
        # Tampilkan Preview Thumbnail Tertinggi
        st.image(resolutions["Max Res (HD - 1080p/720p)"], caption="Preview Thumbnail Utama", use_container_width=True)
        
        # Tombol Download berdasarkan resolusi
        st.subheader("⬇️ Pilih Kualitas Unduhan")
        col1, col2 = st.columns(2)
        
        for i, (res_name, res_url) in enumerate(resolutions.items()):
            with col1 if i % 2 == 0 else col2:
                st.markdown(f"**{res_name}**")
                st.write(f"[Buka & Simpan Gambar]({res_url})")
                
        st.markdown("---")
        
        # --- FITUR REDESIGN / RECREATE PROMPT ---
        st.subheader("🎨 Perintah Recreate / Redesain (AI Prompt)")
        st.write("Gunakan kolom di bawah ini untuk memodifikasi perintah sebelum dimasukkan ke AI (Midjourney, DALL-E, dll).")
        
        # Generate prompt awal berdasarkan judul
        default_prompt = generate_redesign_prompt(video_title)
        
        # Kolom komentar/perintah yang bisa diedit user
        user_prompt = st.text_area(
            "Sesuaikan perintah rekonstruksi thumbnail di sini:", 
            value=default_prompt, 
            height=150
        )
        
        # Instruksi Penggunaan
        st.info(
            "💡 **Cara Pakai:** Salin teks di atas, lalu tempel (*paste*) ke AI Image Generator pilihanmu "
            "(seperti Midjourney, Leonardo.ai, atau Bing Image Creator) untuk membuat aset thumbnail baru yang segar!"
        )
