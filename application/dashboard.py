import streamlit as st

# --- TAMPILAN ---
st.set_page_config(
    page_title = "Dashboard Madrasah Digital",
)
# Header
st.image("https://yt3.googleusercontent.com/6UpF8AEHlaHmxgt5LpSrbcxFbRceiVTfaWLCDyXzEC4Tc4o9Eebcq9bvWAekHqxWvWYsji1hbA=s900-c-k-c0x00ffffff-no-rj", width=200)  # Ganti dengan path logo Anda
st.title("Selamat Datang di Platform Madrasah Digital MAN 2 Jakarta")
st.sidebar.success("Select a page above.")
# Konten Utama
st.write("""
Madrasah Digital adalah platform pembelajaran online yang inovatif dan komprehensif untuk siswa madrasah. 
Kami menyediakan berbagai sumber belajar, latihan interaktif, dan fitur-fitur menarik lainnya untuk mendukung 
perkembangan akademik dan spiritual siswa.
""")


# Footer (Opsional)
st.markdown("---")
st.write("© 2024 MAN 2 Jakarta. Hak Cipta Dilindungi.")
