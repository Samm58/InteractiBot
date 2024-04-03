import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

from htmlTemplates import bot_template, user_template

def get_pdf_txt(pdf_docs):
    txt = ""                            # Storing the text from the pdf
    pdf_reader = PdfReader(pdf_docs)    # Create pdf with pages for each pdf
    for page in pdf_reader.pages:
        page.extract_text()             # Extract all raw text from the pages
        txt += page.extract_text()      # Append to the string
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
        st.error("Please load and analyze a PDF file in the sidebar before querying data.")

def pdf_main():
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    if "pdf_docs" not in st.session_state:
        st.session_state.pdf_docs = None
    if "pdf_uploaded" not in st.session_state:
        st.session_state.pdf_uploaded = False

    user_prompt = st.text_input("Type your query about your documents: ")
    if user_prompt:
        handle_user_input(user_prompt)
        
    with st.sidebar:
        st.image("resources/app_logo.png")
        st.write("# 🗳️ Upload PDF Files")
        pdf_docs = st.file_uploader(
            "Upload your PDF files here", type="pdf")
        if pdf_docs is not None and not st.session_state.pdf_uploaded:
            st.session_state.pdf_docs = pdf_docs
            status_text = st.empty()
            progress_placeholder = st.empty()
            progress_bar = progress_placeholder.progress(0)
            # get the pdf text
            status_text.text("Getting PDF text...")
            raw_txt = get_pdf_txt(st.session_state.pdf_docs)
            progress_bar.progress(25)
            # get the text chuncks
            status_text.text("Getting text chunks...")
            chunks_txt = get_txt_chuncks(raw_txt)
            progress_bar.progress(50)
            # create vector store (knowledge base)
            status_text.text("Creating vector store...")
            vectorstore = get_vectorstore(chunks_txt)
            progress_bar.progress(75)
            # create conversation chain
            status_text.text("Creating conversation chain...")
            st.session_state.conversation = get_conversation_chain(vectorstore)
            progress_bar.progress(100)
            progress_placeholder.empty()
            status_text.empty()
            st.success("✅ PDF Uploaded!")
            st.session_state.pdf_uploaded = True