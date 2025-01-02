import streamlit as st
from PIL import Image
from streamlit_lottie import st_lottie
import requests
import json

st.set_page_config(page_title="Complan AI - Home", page_icon=":house:", layout="wide")

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

def load_lf(filepath: str):
    with open(filepath, "r", encoding='utf-8') as f:
        return json.load(f)

def load_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_coding = load_lf(r"E:\Projects\Complan-AI\src\pages\front.json")

def home():
    col1, col2 = st.columns([3, 2])

    with col1:
        st.title("Welcome to Complan AI :wave:")
        st.header("Your AI-powered Career Companion")
        st.write("""
            Complan AI is designed to help you navigate your career journey with intelligent tools and insights.
            Whether you are planning your next move, evaluating your skills, or seeking new opportunities, Complan AI provides
            personalized recommendations and tools to enhance your professional growth.
        """)

        st.subheader("What Can You Do with Complan AI?")
        st.markdown("""
        - **Competency Planning**: Assess your skills, identify gaps, and get recommendations on how to improve.
        - **Profile Score Calculator**: Calculate a personalized profile score based on your competencies.
        - **Job Market Insights**: Gain insights into the latest job market trends and align your skills with in-demand roles.
        - **Resume Builder**: Create a professional resume with AI-driven suggestions tailored to your skills and experience.
        """)

        st.write("Get started by navigating through the tools on the sidebar. Let Complan AI guide your career to new heights!")

    with col2:
        page_style = """
    <style>
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
    /* Background and text styling to match the animation theme */
    [data-testid="stAppViewContainer"] {
        background-color: #1e1e2f; /* Dark background to match the animation */
        color: #f0f0f7; /* Light text color for contrast */
        padding: 20px; /* Adding some padding for breathing space */
    }
    h1, h2, h3, h4, h5, h6, p, a, label {
        color: #f0f0f7 !important; /* Light color for headers and text */
    }
    .stButton>button {
        background-color: #ff4b4b; /* Bright button color */
        color: #ffffff; /* White text on buttons */
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
    }
    #root {
        background-color: #1e1e2f; /* Dark background */
        padding: 20px;
    }
    .stButton>button:hover {
        background-color: #ff7c7c; /* Lighter on hover */
    }
    [data-testid="stSidebarContent"]{
        background-color: #304463; /* Bright button color */
        color: #ffffff; /* White text on buttons */
        
    }
    .st-markdown {
        font-size: 18px; /* Larger font size for readability */
        line-height: 1.6; /* Better line spacing */
    }
    /* Targeting SVG inside the #root div */
    #root div svg {
        background-color: #1e1e2f; /* Set background color of SVG */
        border-radius: 8px; /* Optional: adds rounded corners */
        padding: 10px; /* Optional: adds padding inside the SVG */
    }
    [data-testid="column"] {
background-color: transparent !important;
}
    </style>
"""
        st.markdown(page_style, unsafe_allow_html=True)
        st_lottie(
            lottie_coding,
            speed=1,
            reverse=False,
            loop=True,
            quality="high",
            height=700,
            width=400,
            key="coding"
        )

if __name__ == "__main__":
    home()
