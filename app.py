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
        
        # 1. Tampilkan Preview Thumbnail
        st.image(resolutions["Max Res (HD - 1080p/720p)"], caption="Preview Thumbnail Utama", use_container_width=True)
        
        st.markdown("---")
        
        # 2. POSISI BARU: FITUR MODIFIKASI & RECREATE PROMPT (Tepat di bawah Gambar)
        st.subheader("🎨 Modifikasi & Recreate Desain")
        st.write("Ketik perintah perubahan yang kamu inginkan di bawah ini tanpa perlu mengedit teks prompt yang rumit.")
        
        # Kolom kosong untuk diisi perintah langsung oleh user
        custom_command = st.text_input(
            "Ketik perintah modifikasi di sini:", 
            placeholder="Contoh: buat background warna merah, tambah efek petir, beri teks 'WAW'"
        )
        
        # Sistem otomatis membuatkan hasil prompt akhirnya
        final_prompt = generate_advanced_prompt(video_title, custom_command)
        
        # Menampilkan hasil siap salin
        st.markdown("**Hasil Prompt AI Siap Salin:**")
        st.code(final_prompt, language="text")
        
        st.info(
            "💡 **Cara Pakai:** Kamu tinggal ketik keinginanmu di kolom atas, lalu klik dua kali atau salin kotak abu-abu di atas "
            "untuk di-paste ke AI Image Generator!"
        )
        
        st.markdown("---")
        
        # 3. POSISI BARU: TOMBOL PILIHAN UNDUHAN (Pindah ke Paling Bawah)
        st.subheader("⬇️ Pilih Kualitas Unduhan")
        col1, col2 = st.columns(2)
        for i, (res_name, res_url) in enumerate(resolutions.items()):
            with col1 if i % 2 == 0 else col2:
                st.markdown(f"**{res_name}**")
                st.write(f"[Buka & Simpan Gambar]({res_url})")
