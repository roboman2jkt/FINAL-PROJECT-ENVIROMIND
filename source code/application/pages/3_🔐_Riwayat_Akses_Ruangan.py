import streamlit as st
import pymongo
import pandas as pd
from fpdf import FPDF
import io
from datetime import datetime

# --- KONEKSI KE MONGODB ---
client = pymongo.MongoClient("mongodb+srv://robotikman2jkt:DdlJaVXGJO4Lo91o@cluster0.knymo2f.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["door_lock"]
collection_log_pintu = db["data_log_pintu_harian"]

# --- TAMPILAN APLIKASI ---
st.title("Data Log Akses Pintu MAN 2 JAKARTA")

# --- FILTER DATA ---
with st.expander("Filter Data"):
    all_rooms = collection_log_pintu.distinct("Ruangan")
    selected_room = st.selectbox("Pilih Ruangan:", all_rooms)

    # Tanggal default 26 Juli 2024
    default_date = datetime(2024, 7, 26).date()
    selected_date = st.date_input("Pilih Tanggal:", value=default_date)

# --- TOMBOL PRINT ---
_, col1, col2, _ = st.columns([1, 1, 1, 1])
with col1:
    if st.button("Print ke PDF"):
        try:
            pdf_output = print_to_pdf(df_logs, selected_room, selected_date)
            st.download_button(
                label="Unduh PDF",
                data=pdf_output,
                file_name=f"log_akses_{selected_room}_{selected_date.strftime('%Y-%m-%d')}.pdf",
                mime="application/pdf",
            )
        except Exception as e:
            st.error(f"Terjadi kesalahan saat mencetak ke PDF: {e}")

with col2:
    if st.button("Print ke XLSX"):
        try:
            xlsx_output = print_to_xlsx(df_logs)
            st.download_button(
                label="Unduh XLSX",
                data=xlsx_output,
                file_name=f"log_akses_{selected_room}_{selected_date.strftime('%Y-%m-%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        except Exception as e:
            st.error(f"Terjadi kesalahan saat mencetak ke XLSX: {e}")

# --- PENGOLAHAN DATA ---
filtered_logs = collection_log_pintu.find({
    "Ruangan": selected_room,
    "Tanggal": selected_date.strftime("%Y-%m-%d")
})
df_logs = pd.DataFrame(list(filtered_logs))

# --- FUNGSI-FUNGSI CETAK ---
def print_to_pdf(df, selected_room, selected_date):
    pdf = FPDF()
    # ... (Kode pembuatan PDF sama seperti sebelumnya) ...

def print_to_xlsx(df):
    xlsx_output = io.BytesIO()
    # ... (Kode pembuatan XLSX sama seperti sebelumnya) ...

# --- TAMPILAN DATA ---
if not df_logs.empty:
    st.write(f"Data Log Akses Ruangan {selected_room} pada {selected_date}")

    st.markdown("""
    <style>
    .dataframe th, .dataframe td {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    df_logs.insert(0, "No.", range(1, len(df_logs) + 1))
    df_logs.rename(columns={"timestamp": "Waktu Akses"}, inplace=True)

    st.write(df_logs[["No.", "Nama", "Ruangan", "Tanggal", "Waktu Akses"]].to_html(escape=False, index=False), unsafe_allow_html=True)

else:
    st.write("Tidak ada data log akses untuk ruangan dan tanggal yang dipilih.")
