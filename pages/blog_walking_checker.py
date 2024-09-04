import streamlit as st
import pandas as pd
from io import StringIO
from services.comment_checker import check_comments

def render():
    st.title("Blog Walking Comment Checker")

    uploaded_file = st.file_uploader("Upload file CSV dengan URL:", type="csv")

    if uploaded_file is not None:
        # Membaca file CSV yang diupload
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        urls = pd.read_csv(stringio).iloc[:, 0].tolist()  # Ambil URL dari kolom pertama CSV

        results = []

        # Memproses setiap URL
        progress_bar = st.progress(0)
        progress_text = st.empty()

        total_urls = len(urls)
        for idx, url in enumerate(urls):
            url = url.strip()
            if check_comments(url):
                results.append({'URL': url, 'Comments Allowed': 'Yes', 'HTML Allowed': 'No'})
            else:
                results.append({'URL': url, 'Comments Allowed': 'No', 'HTML Allowed': 'Yes'})

            # Update progress bar
            progress_bar.progress((idx + 1) / total_urls)
            progress_text.text(f"Progress: {(idx + 1) * 100 // total_urls}% completed")

        # Menampilkan hasil akhir
        df = pd.DataFrame(results)
        st.write("Hasil Blog Walking Comment Checker:")
        st.table(df)

        # Unduh hasil sebagai file Excel
        output_file = StringIO()
        df.to_excel(output_file, index=False)
        output_file.seek(0)

        st.download_button(
            label="Unduh hasil sebagai Excel",
            data=output_file.getvalue(),
            file_name="blog_walking_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
