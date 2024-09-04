import streamlit as st
from services.redirect_services import check_redirect

def render():
    st.header("Redirect Link Checker")

    # User input for URLs and target domain
    urls_input = st.text_area("Masukkan URL (satu per baris):")
    target_domain = st.text_input("Masukkan Target Domain:")

    if st.button("Cek Redirect"):
        urls = urls_input.splitlines()
        results = []
        for url in urls:
            if url.strip():
                result = check_redirect(url.strip(), target_domain)
                results.append((url, "Redirect Benar" if result else "Redirect Salah"))

        st.write("Hasil:")
        for url, status in results:
            st.write(f"{url}: {status}")
