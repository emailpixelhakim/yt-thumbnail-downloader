import streamlit as st
import yt_dlp
import requests
from streamlit.components.v1 import html

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
        except:
            return None

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

st.subheader("🔗 Tautan Video")

# Fitur Utama: Solusi Tombol Paste Menggunakan JavaScript HTML
# Komponen ini akan mendeteksi isi clipboard HP dan langsung mengirimkannya ke input Streamlit
js_paste_helper = """
<script>
function Jspaste() {
    navigator.clipboard.readText().then(text => {
        const inputField = window.parent.document.querySelector('input[aria-label="Masukkan URL Video YouTube:"]');
        if (inputField) {
            inputField.value = text;
            inputField.dispatchEvent(new Event('input', { bubbles: true }));
        }
    }).catch(err => {
        alert("Izinkan akses clipboard di browser HP kamu agar tombol paste berfungsi.");
    });
}
</script>
<button onclick="Jspaste()" style="
    width: 100%; 
    height: 40px; 
    background-color: #262730; 
    color: white; 
    border: 1px solid #464855; 
    border-radius: 4px; 
    cursor: pointer;
    font-weight: bold;
">📋 Paste Otomatis</button>
"""

# Membuat tata letak kolom input dan tombol paste
col_url, col_paste = st.columns([3, 1.2])

with col_url:
    video_url = st.text_input(
        "Masukkan URL Video YouTube:", 
        placeholder="https://www.youtube.com/watch?v=..."
    )

with col_paste:
    st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
    # Memasukkan elemen tombol paste JavaScript
    html(js_paste_helper, height=45)

if video_url:
    with st.spinner("Mengambil data video..."):
        video_data = get_video_info(video_url)
    
    if video_data:
        video_id = video_data["id"]
        video_title = video_data["title"]
        
        st.success(f"Video Ditemukan: **{video_title}**")
        
        # Ambil Gambar Kualitas Tertinggi
        hd_thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        
        # Tampilkan Preview Thumbnail
        st.image(hd_thumbnail_url, caption="Preview Thumbnail Utama", use_container_width=True)
        
        # Eksekusi Download Otomatis
        try:
            response = requests.get(hd_thumbnail_url)
            img_data = response.content
            
            st.download_button(
                label="📥 Download Thumbnail (Kualitas HD)",
                data=img_data,
                file_name=f"thumbnail_{video_id}.jpg",
                mime="image/jpeg",
                use_container_width=True
            )
        except:
            st.warning("Gagal memproses tombol unduh otomatis.")

        st.markdown("---")
        
        # --- RECREATE PROMPT SECTION ---
        st.subheader("🎨 Modifikasi & Recreate Desain")
        st.write("Ketik perintah perubahan yang kamu inginkan di bawah ini:")
        
        col_cmd, col_btn = st.columns([3, 1])
        
        with col_cmd:
            custom_command = st.text_input(
                "Ketik perintah modifikasi di sini:", 
                placeholder="Contoh: buat background warna merah, tambah efek petir",
                label_visibility="collapsed"
            )
        
        if "start_create" not in st.session_state:
            st.session_state.start_create = False
            
        with col_btn:
            if st.button("🚀 Create", type="primary", use_container_width=True):
                st.session_state.start_create = True
        
        if st.session_state.start_create:
            final_prompt = generate_advanced_prompt(video_title, custom_command)
            st.markdown("**Hasil Prompt AI Siap Salin:**")
            st.code(final_prompt, language="text")
            st.success("✅ Klik ikon dua kotak bertumpuk di pojok kanan atas kolom abu-abu untuk COPY instan.")
