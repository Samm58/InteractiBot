import streamlit as st
import openai
import os
from dotenv import load_dotenv
from streamlit_option_menu import option_menu
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

import pandas as pd
from lida import Manager, TextGenerationConfig, llm
from PIL import Image
from io import BytesIO
import base64

from htmlTemplates import css, bot_template, user_template, opt_menu_styles

def get_pdf_txt(pdf_docs):
    txt = ""                            # Storing the text from the pdf
    for pdf in pdf_docs:                # Loop through the pdf and get the content
        pdf_reader = PdfReader(pdf)     # Create pdf with pages for each pdf
        for page in pdf_reader.pages:
            page.extract_text()         # Extract all raw text from the pages
            txt += page.extract_text()  # Append to the string
    return txt                          # Get single string with all the contents from the pdfs


def get_txt_chuncks(txt):
    txt_split = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chuncks = txt_split.split_text(txt)
    return chuncks

def get_vectorstore(chunks_txt):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=chunks_txt, 
                                   embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key='chat_history', 
                                      return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_user_input(user_prompt):
    if st.session_state.conversation is not None:
        response = st.session_state.conversation({'question': user_prompt})
        st.session_state.chat_history = response['chat_history']

        for i, msg in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(user_template.replace("{{MSG}}", msg.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace("{{MSG}}", msg.content), unsafe_allow_html=True)
    else:
        st.write("Please load a CSV file before querying data.")

def base64_to_image(base64_string):
    # Decode the base64 string
    byte_data = base64.b64decode(base64_string)
    # Use BytesIO to convert the byte data to image
    return Image.open(BytesIO(byte_data))

def pdf_main():
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    user_prompt = st.text_input("Type your query about your documents: ")
    if user_prompt:
        handle_user_input(user_prompt)
        
    with st.sidebar:
        st.image("resources/app_logo.png")
        st.write("# 🗳️ Upload PDF Files")
        pdf_docs = st.file_uploader(
            "Upload your PDF files and then click 'Analyze' to load the data",
            type="pdf", 
            accept_multiple_files=True)
        st.write("# ✔️ Click 'Analyze PDF File'")
        if st.button("Analyze PDF File"):
            progress_placeholder = st.empty()
            progress_bar = progress_placeholder.progress(0)
            # get the pdf text
            raw_txt = get_pdf_txt(pdf_docs)
            progress_bar.progress(25)
            # get the text chuncks
            chunks_txt = get_txt_chuncks(raw_txt)
            progress_bar.progress(50)
            # create vector store (knowledge base)
            vectorstore = get_vectorstore(chunks_txt)
            progress_bar.progress(75)
            # create conversation chain
            st.session_state.conversation = get_conversation_chain(vectorstore)
            progress_bar.progress(100)
            progress_placeholder.empty()
            st.success("PDF analysis completed!")
            st.write("# 💬 Chat with you PDF")

def csv_main():
    selected_dataset = None
    with st.sidebar:
        st.image("resources/app_logo.png")
        st.write("# 💡 Choose an Option")
        menu = st.selectbox("Choose an Option", ["Summarization", "Question based Graph"])
        st.write("# 🗳️ Upload a File")
        uploaded_file = st.file_uploader("Upload your file here", type=["csv", "json"])
        if uploaded_file:
            if uploaded_file is not None:
            # Get the original file name and extension
                file_name, file_extension = os.path.splitext(uploaded_file.name)
                # Load the data depending on the file type
                if file_extension.lower() == ".csv":
                    data = pd.read_csv(uploaded_file)
                elif file_extension.lower() == ".json":
                    data = pd.read_json(uploaded_file)
                # Save the data using the original file name in the directory
                uploaded_file_path = os.path.join("file_uploaded", uploaded_file.name)
                data.to_csv(uploaded_file_path, index=False)
                selected_dataset = uploaded_file_path

    if menu == "Summarization" and uploaded_file:
        lida = Manager(text_gen = llm("openai"))
        textgen_config = TextGenerationConfig(n=1, 
                                            temperature=0.5, 
                                            model="gpt-3.5-turbo", 
                                            use_cache=True)
        
        st.subheader("Summarization of your Data")

        summary = lida.summarize(selected_dataset, summary_method="default", textgen_config=textgen_config)
        if "dataset_description" in summary:
            st.write(summary["dataset_description"])

        if "fields" in summary:
            fields = summary["fields"]
            nfields = []
            for field in fields:
                flatted_fields = {}
                flatted_fields["column"] = field["column"]
                for row in field["properties"].keys():
                    if row != "samples":
                        flatted_fields[row] = field["properties"][row]
                    else:
                        flatted_fields[row] = str(field["properties"][row])
                nfields.append(flatted_fields)
            nfields_df = pd.DataFrame(nfields)
            st.write(nfields_df)
        else:
            st.write(str(summary))

        if summary:
            goals = lida.goals(summary, n=2, textgen_config=textgen_config)
            for goal in goals:
                st.write(goal)
            library = "matplotlib"
            textgen_config = TextGenerationConfig(n=1, temperature=0.5, use_cache=True)
            charts = lida.visualize(summary=summary, goal=goals[0], textgen_config=textgen_config, library=library)
            if charts:
                viz_titles = [f'Visualization {i+1}' for i in range(len(charts))]
                img_base64_string = charts[0].raster
                img = base64_to_image(img_base64_string)
                st.image(img, caption=viz_titles, use_column_width=True)
            else:
                st.error("No charts generated")

    elif menu == "Question based Graph" and uploaded_file:
        st.subheader("Query your Data to Generate Graph")
        text_area = st.text_area("Query your Data to Generate Graph", height=100)
        if st.button("Generate Graph"):
            if len(text_area) > 0:
                st.info("Your Query: " + text_area)
                lida = Manager(text_gen = llm("openai")) 
                textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)
                summary = lida.summarize(selected_dataset, summary_method="default", textgen_config=textgen_config)
                user_query = text_area
                library="matplotlib"
                charts = lida.visualize(summary=summary, goal=user_query, textgen_config=textgen_config)
            if charts:
                charts[0]
                image_base64 = charts[0].raster
                img = base64_to_image(image_base64)
                st.image(img)
            else:
                st.error("No charts generated. Try again with better prompt")

if __name__ == '__main__':
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    st.set_page_config(
        page_title ="PetroBot",
        page_icon="resources\petrobot_icon.png",
        layout='wide')
    st.write("<h1 style='text-align: center; color: white;'>Welcome to InteractiBot! 🤖</h1>", unsafe_allow_html=True)
    st.write("<h3 style='text-align: center; color: white;'>Your interactive gateway to seamless PDF and CSV file management and analysis with AI Chat</h3>", unsafe_allow_html=True)
    st.write(css, unsafe_allow_html=True)
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

