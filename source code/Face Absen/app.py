import streamlit as st
import pymongo
import pandas as pd
import streamlit_shadcn_ui as ui

# Koneksi ke MongoDB
client = pymongo.MongoClient("mongodb+srv://robotikman2jkt:DdlJaVXGJO4Lo91o@cluster0.knymo2f.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["data_presensi"]  # Ganti dengan nama database Anda
collection_kehadiran = db["data_siswa_harian"]  # Koleksi untuk data kehadiran harian
collection_siswa = db["data_siswa"]  # Koleksi untuk data seluruh siswa

st.header("Tes Data Presensi MAN 2 JAKARTA")

# Dapatkan semua kelas yang unik
all_classes = collection_siswa.distinct("class")  # Ambil dari collection_siswa

# Filter kelas dan tanggal
selected_class = st.selectbox("Pilih Kelas", all_classes)
selected_date = st.date_input("Pilih Tanggal")

# Ambil data kehadiran berdasarkan filter
filtered_kehadiran = collection_kehadiran.find({
    "class": selected_class,
    "date": selected_date.strftime("%Y-%m-%d")
})
df_kehadiran = pd.DataFrame(list(filtered_kehadiran))

# Ambil data seluruh siswa dalam kelas yang dipilih
siswa_kelas = collection_siswa.find({"class": selected_class})
df_siswa = pd.DataFrame(list(siswa_kelas))

# Buat kamus untuk menyimpan status kehadiran berdasarkan nama
status_kehadiran = {}
for _, row in df_kehadiran.iterrows():
    status_kehadiran[row["name"]] = {
        "status": "HADIR",
        "timestamp": row["timestamp"],
        "date": row["date"]
    }

df_siswa.index += 1
# Gabungkan status kehadiran ke DataFrame siswa
df_siswa["status"] = df_siswa["name"].apply(lambda x: status_kehadiran.get(x, {"status": "TIDAK HADIR"})["status"])
df_siswa["timestamp"] = df_siswa["name"].apply(lambda x: status_kehadiran.get(x, {"timestamp": None})["timestamp"])
df_siswa["date"] = df_siswa["name"].apply(lambda x: status_kehadiran.get(x, {"date": selected_date.strftime("%Y-%m-%d")})["date"])

# Logika untuk menentukan status kehadiran (contoh sederhana)
for index, row in df_siswa.iterrows():
    if row["timestamp"] and row["timestamp"] > "08:00:00":
        df_siswa.at[index, "status"] = "TERLAMBAT"

# Tampilkan DataFrame
st.write(f"Data Presensi Kelas {selected_class} pada {selected_date}")
st.table(df_siswa[["name", "class", "status", "date", "timestamp"]])