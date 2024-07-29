import streamlit as st
import pymongo
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# --- KONEKSI KE MONGODB ---
client = pymongo.MongoClient("mongodb+srv://robotikman2jkt:DdlJaVXGJO4Lo91o@cluster0.knymo2f.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["data_presensi"]
collection_kehadiran = db["data_siswa_harian"]
collection_siswa = db["data_siswa"]

# --- TAMPILAN APLIKASI ---
st.title("Data Presensi MAN 2 JAKARTA")

# Filter Data
with st.expander("Filter Data"):
    selected_class = st.selectbox("Pilih Kelas:", collection_siswa.distinct("class"))
    # Tanggal default 26 Juli 2024
    default_date = datetime(2024, 7, 26).date()
    selected_date = st.date_input("Pilih Tanggal:", value=default_date)

# Tombol Print (di bawah filter)
_, col1, col2, _ = st.columns([1, 1, 1, 1])  # Menciptakan 4 kolom, 2 kolom di tengah untuk tombol
with col1:
    if st.button("Print ke XLSX"):
        try:
            df_siswa_export = df_siswa[["No.", "Nama", "Kelas", "status", "Tanggal", "Waktu Presensi"]].copy()
            df_siswa_export["status"] = df_siswa_export["status"].apply(lambda x: x[x.find(">")+1:x.rfind("<")])  
            df_siswa_export.to_excel("data_presensi.xlsx", index=False)
            st.success("File XLSX berhasil disimpan!")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat mencetak ke XLSX: {e}")

with col2:
    if st.button("Print ke PDF"):
        try:
            # Membuat objek PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=10)  # Ubah ukuran font menjadi lebih kecil

            # Menambahkan judul
            pdf.cell(0, 10, txt=f"Data Presensi Kelas {selected_class} pada {selected_date}", ln=1, align="C")
            pdf.ln(5)  # Tambahkan sedikit jarak setelah judul

            # Menghitung lebar kolom
            col_width = pdf.w / 6  # 6 kolom

            # Menambahkan header tabel (tanpa badge HTML)
            for col in df_siswa[["No.", "Nama", "Kelas", "status", "Tanggal", "Waktu Presensi"]].columns:
                pdf.cell(col_width, 10, txt=col, border=1, align="C")
            pdf.ln(10)

            # Menambahkan data ke tabel
            for _, row in df_siswa[["No.", "Nama", "Kelas", "status", "Tanggal", "Waktu Presensi"]].iterrows():
                for item in row:
                    if isinstance(item, str) and item.startswith("<span"):
                        item = item[item.find(">")+1:item.rfind("<")]
                    pdf.cell(col_width, 10, txt=str(item), border=1, align="C")
                pdf.ln()

            # Menyimpan file PDF
            pdf.output("data_presensi.pdf")
            st.success("File PDF berhasil disimpan!")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat mencetak ke PDF: {e}")

# --- PENGOLAHAN DATA ---
# Ambil data kehadiran berdasarkan filter
filtered_kehadiran = collection_kehadiran.find({
    "class": selected_class,
    "date": selected_date.strftime("%Y-%m-%d")
})
df_kehadiran = pd.DataFrame(list(filtered_kehadiran))

# Ambil data siswa
siswa_kelas = collection_siswa.find({"class": selected_class})
df_siswa = pd.DataFrame(list(siswa_kelas))

# Menggabungkan data kehadiran dan data siswa
status_kehadiran = {row["name"]: {"status": "HADIR", "timestamp": row["timestamp"], "date": row["date"]} for _, row in df_kehadiran.iterrows()}
df_siswa["status"] = df_siswa["name"].apply(lambda x: status_kehadiran.get(x, {"status": "TIDAK HADIR"})["status"])
df_siswa["timestamp"] = df_siswa["name"].apply(lambda x: status_kehadiran.get(x, {"timestamp": None})["timestamp"])
df_siswa["date"] = df_siswa["name"].apply(lambda x: status_kehadiran.get(x, {"date": selected_date.strftime("%Y-%m-%d")})["date"])

# Menandai siswa yang terlambat
for index, row in df_siswa.iterrows():
    if row["timestamp"] and row["timestamp"] > "06:40:00":
        df_siswa.at[index, "status"] = "TERLAMBAT"

# Ganti nama kolom (sebelum menambahkan kolom No.)
df_siswa = df_siswa.rename(columns={
    "name": "Nama",
    "class": "Kelas",
    "date": "Tanggal",
    "timestamp": "Waktu Presensi"
})

# Tambahkan kolom "No." (setelah mengganti nama kolom)
df_siswa.insert(0, "No.", range(1, len(df_siswa) + 1))

# --- TAMPILAN DATA ---
# Styling CSS (tidak berubah)
st.markdown("""
<style>
.badge {
    padding: 5px 10px;
    border-radius: 5px;
    font-weight: bold;
    white-space: nowrap;
    display: inline-block;
    vertical-align: middle;
}
.badge-hadir {
    background-color: #3B82F6;
    color: white;
}
.badge-terlambat {
    background-color: #EF4444;
    color: white;
}
.badge-tidak-hadir {
    background-color: #D1D5DB;
    color: black;
}
/* CSS untuk mengatur header dan teks menjadi rata tengah */
.dataframe th, .dataframe td {
    text-align: center; 
}
</style>
""", unsafe_allow_html=True)

# Buat salinan df_siswa untuk memodifikasi kolom status
df_siswa_styled = df_siswa.copy()  

# Modifikasi kolom "status" menjadi badge HTML dengan class CSS
df_siswa_styled["Status"] = df_siswa_styled["status"].apply(lambda status:
    f'<span class="badge badge-{status.lower().replace(" ", "-")}">{status}</span>'
)

# Mengganti nilai None pada kolom Waktu Presensi menjadi "Tidak Ada"
df_siswa_styled['Waktu Presensi'] = df_siswa_styled['Waktu Presensi'].fillna("Tidak Ada")

# Menampilkan DataFrame
st.write(f"Data Presensi Kelas {selected_class} pada {selected_date}")
styled_df = df_siswa_styled[["No.", "Nama", "Kelas", "Status", "Tanggal", "Waktu Presensi"]].style.set_properties(**{
    'text-align': 'center'
})
st.write(df_siswa_styled[["No.", "Nama", "Kelas", "Status", "Tanggal", "Waktu Presensi"]].to_html(escape=False, index=False), unsafe_allow_html=True)
