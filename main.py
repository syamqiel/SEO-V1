import streamlit as st
import pandas as pd
from io import BytesIO
from io import StringIO
from services.comment_checker import check_comments
from services.ping_services import ping_all_services
from services.redirect_services import check_backlinks

# Mengatur layout halaman menjadi lebar
st.set_page_config(layout="wide")

# Judul Aplikasi
st.title("SEO TOOLS V.1")
st.write("Selamat datang di aplikasi multi-fitur! Untuk SEO Optimation di sini Anda dapat memeriksa komentar blog, ping tools, dan redirect checker di satu halaman.")

# Fungsi untuk menyimpan DataFrame ke file Excel di memori
def save_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Results')
    output.seek(0)
    return output

# Tabs untuk membedakan setiap fitur
tabs = st.tabs(["Blog Comment Checker", "Ping Tools", "Redirect Checker"])

# Tab Blog Comment Checker
with tabs[0]:
    st.header("Blog Comment Checker")

    # Pilihan untuk input
    input_choice = st.radio("Pilih metode input:", ('Upload file CSV', 'Input langsung'))

    urls = []
    if input_choice == 'Upload file CSV':
        uploaded_file = st.file_uploader("Upload file CSV dengan URL:", type="csv")
        
        if uploaded_file is not None:
            # Membaca file CSV yang diupload
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            urls = pd.read_csv(stringio).iloc[:, 0].tolist()  # Ambil URL dari kolom pertama CSV

    elif input_choice == 'Input langsung':
        urls_input = st.text_area("Masukkan daftar URL (pisahkan dengan baris baru):", height=200)
        urls = [url.strip() for url in urls_input.split('\n') if url.strip()]

    # Memeriksa jika ada URL yang dimasukkan
    if st.button("Cek Komentar"):
        if urls:
            results = []
            total_urls = len(urls)

            # Progress Bar
            progress_bar = st.progress(0)
            progress_text = st.empty()

            for idx, url in enumerate(urls):
                result = check_comments(url)
                results.append({
                    'URL': url,
                    'Comments Allowed': result['comments_allowed'],
                    'Backlink Allowed': result['backlink_allowed']
                })

                # Update progress bar setiap kali satu URL selesai diproses
                progress_bar.progress((idx + 1) / total_urls)
                progress_text.text(f"Proses: {((idx + 1) * 100) // total_urls}% selesai")

            # Menghapus progress bar setelah proses selesai
            progress_bar.empty()

            # Menampilkan hasil ke dalam tabel
            df = pd.DataFrame(results)
            st.write("Hasil Blog Comment Checker:")

            # Menambahkan emoji centang dan silang di kolom 'Comments Allowed' dan 'Backlink Allowed'
            df['Comments Allowed'] = df['Comments Allowed'].apply(lambda x: '✅' if x else '❌')
            df['Backlink Allowed'] = df['Backlink Allowed'].apply(lambda x: '✅' if x else '❌')

            # Menampilkan tabel dalam format dataframe interaktif
            st.dataframe(df)

            # Unduh hasil sebagai file Excel
            output_file = save_to_excel(df)

            st.download_button(
                label="Unduh hasil sebagai Excel",
                data=output_file,
                file_name="blog_comment_results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("Masukkan setidaknya satu URL.")

# Tab Ping Tools
with tabs[1]:
    st.header("Ping Tools")
    st.write("Masukkan daftar URL yang ingin diping (pisahkan dengan baris baru):")

    # Menggunakan text_area agar bisa input lebih dari satu URL
    urls_ping_input = st.text_area("Daftar URL:", height=200, placeholder="https://example.com")

    category = st.selectbox("Pilih kategori:", [
        "Other", "Financial", "Business", "Education", 
        "Entertainment", "Family", "Information", 
        "Technology", "Tips and Trick", "Internet & Online"
    ])

    # Tombol untuk melakukan ping
    if st.button("Ping URL"):
        if urls_ping_input:
            # Memisahkan input menjadi daftar URL
            urls_ping = [url.strip() for url in urls_ping_input.split('\n') if url.strip()]

            if not urls_ping:
                st.warning("Masukkan setidaknya satu URL yang valid.")
            else:
                total_urls = len(urls_ping)
                progress_bar = st.progress(0)
                progress_text = st.empty()

                # Memproses setiap URL yang dimasukkan
                for idx, url_ping in enumerate(urls_ping):
                    st.write(f"Website URL: {url_ping}")

                    services_result = ping_all_services(url_ping, category)
                    
                    # Menyusun hasil menjadi DataFrame
                    result_df = pd.DataFrame(services_result, columns=['Source', 'Status'])

                    # Menampilkan hasil dalam tabel
                    st.table(result_df)

                    st.write("------ COMPLETED ------")

                    # Update progress bar
                    progress_bar.progress((idx + 1) / total_urls)
                    progress_text.text(f"Proses: {(idx + 1) * 100 // total_urls}% selesai")

                # Menghapus progress bar setelah selesai
                progress_bar.empty()
        else:
            st.warning("Masukkan setidaknya satu URL.")

# Tab Redirect Checker
with tabs[2]:
    st.header("Redirect Checker")
    st.write("Masukkan target domain (contoh: telkomuniversity.ac.id):")
    target_domain = st.text_input('Target Domain', '')

    # Input Box untuk URL List
    st.write("Masukkan daftar URL (pisahkan dengan baris baru):")
    url_input = st.text_area('Daftar URL', '', height=300)  # Tinggi diset agar textarea lebih besar

    # Tombol untuk Mengeksekusi Pemeriksaan
    if st.button('Cek Redirect'):
        # Memproses daftar URL dari input user
        urls = [url.strip() for url in url_input.split('\n') if url.strip()]

        if urls and target_domain:
            total_urls = len(urls)
            # Menampilkan progress bar dan teks kemajuan
            progress_bar = st.progress(0)
            progress_text = st.empty()  # Placeholder untuk teks kemajuan

            # Memanggil fungsi check_backlinks dari redirect_services.py
            results, redirect_count, invalid_count = check_backlinks(urls, target_domain)

            for idx in range(total_urls):
                # Update progress bar
                progress_bar.progress((idx + 1) / total_urls)
                progress_text.text(f"Proses: {(idx + 1) * 100 // total_urls}% selesai")

            # Menghapus progress bar setelah selesai
            progress_bar.empty()
            progress_text.empty()

            # Menyiapkan hasil ke dalam DataFrame dengan emoji
            df = pd.DataFrame(results, columns=['URL', 'Redirects to Target'])

            # Menambahkan emoji centang dan silang di kolom 'Redirects to Target'
            df['Redirects to Target'] = df['Redirects to Target'].apply(lambda x: '✅' if x else '❌')

            # Menambahkan kolom Status untuk error handling
            df['Status'] = ['Valid' if x else 'No Backlink or Error' for x in df['Redirects to Target'].map(lambda x: x == '✅')]

            # Menampilkan DataFrame ke layar dengan styling sederhana
            st.write("### Hasil Pemeriksaan:")
            st.dataframe(df)

            # Menyimpan ke file Excel
            excel_data = save_to_excel(df)

            # Membuat tombol unduh untuk file Excel
            st.download_button(label='Download hasil pengecekan',
                            data=excel_data,
                            file_name='redirect_check_results.xlsx',
                            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

            # Menampilkan statistik dengan penekanan visual
            st.markdown("### Statistik Hasil:")
            st.write(f"**Total valid links redirecting to {target_domain}:** {redirect_count}")
            st.write(f"**Total invalid links:** {invalid_count}")
            st.write(f"**Total links processed:** {len(results)}")
        else:
            st.warning("Masukkan setidaknya satu URL.")

