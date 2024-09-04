import streamlit as st
from pages import ping_tools, blog_walking_checker

def main():
    st.title("Aplikasi Multi-Fitur")

    # Buat tab sebagai navigasi horizontal
    tabs = st.tabs(["Ping Tools", "Blog Walking Comment Checker"])

    with tabs[0]:
        ping_tools.render()
    with tabs[1]:
        blog_walking_checker.render()

if __name__ == "__main__":
    main()


    