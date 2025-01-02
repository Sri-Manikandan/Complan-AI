import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import DeepLake
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI

st.set_page_config(page_title="Candidate AI", page_icon="🧠")

Page_style = """
    <style>
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
   
    /* Background and text styling to match the animation theme */
    [data-testid="stAppViewContainer"] {
        background-color: #1e1e2f; /* Dark background to match the animation */
        color: #f0f0f7; /* Light text color for contrast */
    }
    h1, h2, h3, h4, h5, h6, p, a, label {
        color: #f0f0f7 !important; /* Light color for headers and text */
    }
     [data-testid="stSidebarCollapseButton"]{
        background-color: #304463; /* Bright button color */
        color: #ffffff; /* White text on buttons */
        
    }
    [data-testid="stSidebarContent"]{
        background-color: #304463; /* Bright button color */
        color: #ffffff; /* White text on buttons */
        
    }
    .st-emotion-cache-1itdyc2{
       background-color: #304463; 
    }
       [data-testid="stSidebarNav"] {
        background-color: #304463; /* Dark background for sidebar */
        ; /* Add padding around the sidebar */
        border-radius: 10px; /* Rounded corners for a smooth look */
    }

    /* Styling each navigation link */
    [data-testid="stSidebarNavLink"] {
        background-color:black; /* Darker background for each link */
        color: #f0f0f7 !important; /* Light text color */
        padding: 12px 20px; /* Add padding to the links */
        border-radius: 8px; /* Rounded corners for links */
        text-decoration: none; /* Remove underline */
        display: block; /* Make the link take full width */
        margin-bottom: 10px; /* Space between links */
        transition: background-color 0.3s ease; /* Smooth transition */
    }
.st-emotion-cache-6qob1r {
    position: relative;
    height: 100%;
    width: 100%;
    overflow: overlay;}
    /* Styling the hover effect on the navigation links */
    [data-testid="stSidebarNavLink"]:hover {
        background-color: #3d3d5c; /* Slightly lighter background on hover */
    }

    /* Styling the text inside the navigation links */
    [data-testid="stSidebarNavLink"] span {
        font-weight: bold; /* Make the text bold */
        font-size: 16px; /* Slightly larger font size */
    }

    /* Remove the default list style */
    [data-testid="stSidebarNavItems"] {
        list-style-type: none;
        padding: 0;
    }
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #2e2e3e;
    }
    
    ::-webkit-scrollbar-thumb {
        background-color: #555555;
        border-radius: 6px;
        border: 3px solid #2e2e3e;
    }
    .MuiBox-root ,.css-0{
    background-color:#1e1e2f;
    }
    </style>
"""
st.markdown(Page_style,unsafe_allow_html=True)

load_dotenv()

def get_pdf_text(pdf):
    text = ""
    pdfReader = PdfReader(pdf)
    for page in pdfReader.pages:
        text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=750,
        chunk_overlap=50,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    dataset_path = "./my_deeplake_candidate/"
    vectorstore = DeepLake.from_texts(text_chunks,dataset_path=dataset_path, embedding=OpenAIEmbeddings())
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI(model="gpt-4o")
    memory = ConversationBufferMemory(memory_key='chat_history',return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        memory=memory,
        retriever=vectorstore.as_retriever(),
    )
    return conversation_chain

def handle_defaultinput(user_question):
    response  = st.session_state.conversation({'question':user_question})
    st.session_state.response1 = response['answer']

def main():
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    if "response1" not in st.session_state:
        st.session_state.response1 = ""

    st.header('Job Recommender')
    st.subheader('AI Based Job Recommendation system to analyse job seeker profiles and find suitable job opportunities for the particular resume.')

    with st.sidebar:
        st.subheader('Your Resume')
        pdf = st.file_uploader('Upload your resume:')
        if st.button('Process'):
            with st.spinner('Processing...'):
                raw_text = get_pdf_text(pdf)

                text_chunks = get_text_chunks(raw_text)

                vectorstore = get_vectorstore(text_chunks)

                st.session_state.conversation = get_conversation_chain(vectorstore)
                handle_defaultinput('Suggest best suited job for this resume by providing the two best job options and expected salary in rupees in about 50 words')
                DeepLake.force_delete_by_path("./my_deeplake_candidate")
        st.divider()
    
    st.write(st.session_state.response1)

if __name__ == '__main__':
    main()