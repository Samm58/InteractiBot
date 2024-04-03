import streamlit as st
import openai
import os
from dotenv import load_dotenv
from streamlit_option_menu import option_menu
from langchain_pdf import pdf_main
from lida_csv import csv_main
from htmlTemplates import css, opt_menu_styles

if __name__ == '__main__':
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    st.set_page_config(
        page_title ="InteractiBot",
        page_icon="resources\interactibot_icon.png",
        layout='wide')
    st.markdown(css, unsafe_allow_html=True)
    st.markdown("<h1 class='my-title'> Welcome to InteractiBot! 🤖</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='my-title'> Your interactive gateway to seamless PDF and CSV file management and analysis with AI Chat</h2>", unsafe_allow_html=True)
    st.markdown("<h3 class='my-subtitle'> Ready? Choose file type you would like to interact with:</h3>", unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None,
        options=["CSV", "PDF"],
        icons=["filetype-csv", "filetype-pdf"],
        orientation="horizontal",
        styles=opt_menu_styles)
    
    if selected == "PDF":
        pdf_main()
    if selected == "CSV":
        csv_main()

