import streamlit as st
from pages import ping_tools, blog_walking_checker

def main():
    # Sidebar menu untuk navigasi
    st.sidebar.title("Menu")
    menu = st.sidebar.radio("Pilih fitur", ["Ping Tools", "Blog Walking Comment Checker"])

    # Navigasi ke fitur yang dipilih
    if menu == "Ping Tools":
        ping_tools.render()
    elif menu == "Blog Walking Comment Checker":
        blog_walking_checker.render()

if __name__ == "__main__":
    main()
