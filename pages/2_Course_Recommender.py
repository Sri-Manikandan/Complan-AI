import base64
import os
import requests
import streamlit as st
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import DeepLake
from langchain_google_genai import (ChatGoogleGenerativeAI,
                                    GoogleGenerativeAIEmbeddings)
from PyPDF2 import PdfReader

load_dotenv()

page_style = """
    <style>
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
   
    /* Background and text styling to match the animation theme */
    [data-testid="stAppViewContainer"] {
        background-color: #1e1e2f; /* Dark background to match the animation */
        color: #f0f0f7; /* Light text color for contrast *//
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
    </style>
"""
st.markdown(page_style, unsafe_allow_html=True)

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
    vectorstore = DeepLake.from_texts(text_chunks, dataset_path=dataset_path, embedding=GoogleGenerativeAIEmbeddings(model="models/embedding-001"))
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        memory=memory,
        retriever=vectorstore.as_retriever(),
    )
    return conversation_chain

def get_auth_header(client_id, client_secret):
    auth_str = f"{client_id}:{client_secret}"
    auth_bytes = auth_str.encode("ascii")
    auth_base64 = base64.b64encode(auth_bytes).decode("ascii")
    return {"Authorization": f"Basic {auth_base64}"}

def fetch_udemy_courses(auth_header, query="", fields="", page_size=5):
    base_url = "https://www.udemy.com/api-2.0/courses/"
    params = {
        "search": query,
        "page": 1,
        "page_size": page_size,
        "fields[course]": fields
    }
    response = requests.get(base_url, headers=auth_header, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch courses: {response.status_code}")
        return None

def generate_courses(job_role, work_experience, resume):
    raw_text = get_pdf_text(resume)
    text_chunks = get_text_chunks(raw_text)
    vectorstore = get_vectorstore(text_chunks)
    chain = get_conversation_chain(vectorstore)
    
    prompt = f'''
    You are an experienced Human Resource Manager and Courses recommender. 
    Analyze and extract the skills from the resume of the candidate. Output only the technical skills.
    '''
    response1 = chain({'question': prompt})
    
    missing_skills_prompt = f'''
    Based on the job role {job_role} and work experience {work_experience}, 
    and the skills identified in the resume ({response1['answer']}), 
    identify any missing technical skills.
    '''
    response2 = chain({'question': missing_skills_prompt})
    missing_skills = response2['answer']

    st.subheader("Skills Gap Analysis:")
    st.write(missing_skills)
    
    client_id = os.getenv("UDEMY_CLIENT_ID")
    client_secret = os.getenv("UDEMY_CLIENT_SECRET")
    fields = "title,headline,url,num_subscribers,avg_rating,price"

    if client_id and client_secret:
        auth_header = get_auth_header(client_id, client_secret)
        courses = fetch_udemy_courses(auth_header, query=missing_skills, fields=fields)
        if courses:
            st.header(f"Courses to Improve your skills:")
            for course in courses.get('results', []):
                st.markdown(f"""
    <div style="
        border: 2px solid #34344a;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        background-color: #1e1e2f;
        color: #f0f0f7;
    ">
        <h3 style="color: #ff4b4b;">Title: {course['title']}</h3>
        <p><strong>Headline:</strong> {course['headline']}</p>
        <p><strong>Number of Subscribers:</strong> {course['num_subscribers']}</p>
        <p><strong>Average Rating:</strong> {course['avg_rating']}</p>
        <p><strong>Price:</strong> {course['price']}</p>
        <a href="https://www.udemy.com{course['url']}" style="color: #ff4b4b; text-decoration: none; font-weight: bold;">
            View Course
        </a>
    </div>
    """, unsafe_allow_html=True)
                # st.subheader(f"**Title:** {course['title']}")
                # st.write(f"**Headline:** {course['headline']}")
                # st.write(f"**Number of Subscribers:** {course['num_subscribers']}")
                # st.write(f"**Average Rating:** {course['avg_rating']}")
                # st.write(f"**Price:** {course['price']}")
                # st.write(f"[View Course](https://www.udemy.com{course['url']})")
    
    DeepLake.force_delete_by_path("./my_deeplake_candidate")

def start():
    st.title("Course Recommender")
    st.write("Welcome to the Course Recommender. Please enter the details below to get the skill gap analysis and courses that you can take to improve your skills.")
    with st.sidebar:
        job_role = st.text_input("Job Role")
        work_experience = st.text_input("Work Experience")
        resume = st.file_uploader("Upload Resume")

    submit = st.button("Submit")
    if submit:
        with st.spinner('Processing...'):
            generate_courses(job_role, work_experience, resume)

if __name__ == "__main__":
    start()
