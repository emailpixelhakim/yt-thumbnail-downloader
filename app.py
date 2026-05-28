import streamlit as st
import re
import requests

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="YT Thumbnail Downloader & Redesigner", page_icon="📸", layout="centered")

def extract_video_id(url):
    """Mengekstrak ID video dari berbagai model URL YouTube secara instan"""
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)
    if match:
        return match.group(1)
    return None

def get_video_title_fallback(video_id):
    """Mengambil judul video secara cepat lewat oEmbed API resmi YouTube"""
    try:
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            return res.json().get("title", "YouTube Video")
    except:
        pass
    return "YouTube Video"

def generate_advanced_prompt(title, user_instruction):
    """Menggabungkan judul video dengan instruksi custom dari user"""
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

# 1. Bagian Tautan Video
st.subheader("🔗 Tautan Video")
video_url = st.text_input(
    "Masukkan URL Video YouTube:", 
    placeholder="https://www.youtube.com/watch?v=... atau https://youtu.be/..."
)

if video_url:
    video_id = extract_video_id(video_url)
    
    if video_id:
        with st.spinner("Mengambil informasi video..."):
            video_title = get_video_title_fallback(video_id)
        
        st.success(f"🎥 Video Ditemukan: **{video_title}**")
        
        # Link Gambar Kualitas Tertinggi (HD)
        hd_thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        fallback_thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        
        # 2. Tampilkan Preview Thumbnail Utama
        st.image(hd_thumbnail_url, caption="Preview Thumbnail Utama", use_container_width=True)
        
        # 3. SATU TOMBOL DOWNLOAD HD (Tepat di bawah preview gambar)
        try:
            response = requests.get(hd_thumbnail_url, timeout=5)
            if response.status_code != 200:
                response = requests.get(fallback_thumbnail_url, timeout=5)
            img_data = response.content
            
            st.download_button(
                label="📥 Download Thumbnail (Kualitas HD)",
                data=img_data,
                file_name=f"thumbnail_{video_id}.jpg",
                mime="image/jpeg",
                use_container_width=True
            )
        except:
            st.warning("Gagal memproses unduhan otomatis. Silakan ketuk lama gambar preview di atas lalu simpan ke galeri.")

        st.markdown("---")
        
        # 4. KOLOM PERINTAH MODIFIKASI
        st.subheader("🎨 Modifikasi & Recreate Desain")
        custom_command = st.text_input(
            "Ketik perintah modifikasi di sini:", 
            placeholder="Contoh: buat background warna merah, tambah efek petir, beri teks 'WAW'"
        )
        
        # 5. HASIL PROMPT YANG SIAP DI-COPY (Tepat di bawah perintah)
        final_prompt = generate_advanced_prompt(video_title, custom_command)
        
        st.markdown("**Hasil Prompt AI Siap Salin:**")
        # Menggunakan st.code agar muncul tombol "Copy" otomatis di pojok kanan atas kotaknya
        st.code(final_prompt, language="text")
        st.info("💡 Klik ikon kotak bertumpuk di pojok kanan atas kolom abu-abu di atas untuk menyalin instan.")
        
    else:
        st.error("Format link YouTube tidak dikenali. Pastikan tautan yang dimasukkan benar.")
