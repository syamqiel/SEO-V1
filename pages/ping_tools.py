import streamlit as st
import pandas as pd
from services.ping_services import ping_all_services

def render():
    st.title("Ping Tools")

    # Input dari pengguna
    urls = st.text_area("Masukkan URL (satu URL per baris):")
    category = st.selectbox("Pilih Kategori:", ["Other", "News", "Blogs", "Technology", "Business"])

    if st.button("Kirim Ping"):
        url_list = [url.strip() for url in urls.splitlines() if url.strip()]
        total_urls = len(url_list)

        # Progress bar tunggal untuk semua URL
        progress_bar = st.progress(0)
        progress_text = st.empty()

        all_results = []
        for idx, url in enumerate(url_list):
            st.subheader(f"Website URL: {url}")
            results = ping_all_services(url, category)
            all_results.extend([(url, result[0], result[1]) for result in results])

            # Update progress bar
            progress_bar.progress((idx + 1) / total_urls)
            progress_text.text(f"Progress: {(idx + 1) * 100 // total_urls}% completed")

        # Menampilkan hasil akhir
        if all_results:
            df = pd.DataFrame(all_results, columns=["URL", "Source", "Status"])
            st.table(df)
