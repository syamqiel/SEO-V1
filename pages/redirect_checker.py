import streamlit as st
import pandas as pd
from services import redirect_services

def render():
    st.header("Redirect Link Checker")

    # Input links dari pengguna
    link_input = st.text_area("Masukkan link (satu link per baris)", height=200)
    target_domain = st.text_input("Masukkan target domain (contoh: telkomuniversity.ac.id)")

    # Tombol untuk mulai memeriksa link
    if st.button("Periksa Redirect"):
        links = link_input.strip().splitlines()  # Memisahkan input menjadi list
        if links and target_domain:
            # Memanggil layanan untuk memeriksa redirect
            results = redirect_services.check_backlinks(links, target_domain)

            # Membuat DataFrame dari hasil
            df = pd.DataFrame(results, columns=['Link', 'Status'])
            df.index = df.index + 1  # Mengatur indeks agar dimulai dari 1

            # Menampilkan tabel
            st.table(df)

            # Ekspor ke Excel
            if st.button("Ekspor ke Excel"):
                output_file_path = "redirect_results.xlsx"
                df.to_excel(output_file_path, index=True)
                st.success(f"Hasil telah diekspor ke {output_file_path}")
        else:
            st.warning("Silakan masukkan link dan target domain terlebih dahulu.")
