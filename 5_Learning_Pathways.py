import base64
import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Udemy API credentials from environment variables
UD_API_CLIENT_ID = os.getenv("UDEMY_CLIENT_ID")
UD_API_CLIENT_SECRET = os.getenv("UDEMY_CLIENT_SECRET")

# Function to generate the authentication header for the Udemy API
def get_auth_header(client_id, client_secret):
    auth_str = f"{client_id}:{client_secret}"
    auth_bytes = auth_str.encode("ascii")
    auth_base64 = base64.b64encode(auth_bytes).decode("ascii")
    return {"Authorization": f"Basic {auth_base64}"}

# Function to fetch Udemy courses for a specific query
def fetch_udemy_courses(auth_header, query="", fields="", page_size=1):
    base_url = "https://www.udemy.com/api-2.0/courses/"
    params = {
        "search": query,
        "page": 1,
        "page_size": page_size,  # Fetch only one course for each tech stack
        "fields[course]": fields
    }
    response = requests.get(base_url, headers=auth_header, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch courses: {response.status_code}")
        return None

# Function to display course recommendations for a specific tech stack
def display_course_recommendations(tech):
    client_id = UD_API_CLIENT_ID
    client_secret = UD_API_CLIENT_SECRET
    fields = "title,headline,url,num_subscribers,avg_rating,price"
    
    if client_id and client_secret:
        auth_header = get_auth_header(client_id, client_secret)
        courses = fetch_udemy_courses(auth_header, query=tech, fields=fields)
        if courses:
            course = courses['results'][0]  # Get the top course
            st.write(f"**Title:** {course['title']}")
            st.write(f"**Headline:** {course['headline']}")
            st.write(f"**Number of Subscribers:** {course['num_subscribers']}")
            st.write(f"**Average Rating:** {course['avg_rating']}")
            st.write(f"**Price:** {course['price']}")
            st.write(f"[View Course](https://www.udemy.com{course['url']})")
            st.markdown("---")

def start():
    st.title("Technical Stack Roadmap with Course Recommendations")

    roadmap = {
        "Frontend": ["HTML", "CSS", "JavaScript", "React", "Vue.js", "Angular"],
        "Backend": ["Node.js", "Express", "Django", "Flask", "Ruby on Rails"],
        "DevOps": ["Docker", "Kubernetes", "CI/CD", "AWS", "Azure", "GCP"],
        "Databases": ["MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite"],
        "Others": ["Python", "Java", "C++", "TypeScript", "Git"]
    }
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
    .MuiBox-root ,.css-0{
    background-color:#1e1e2f;
    }
    </style>
"""
    st.markdown(page_style, unsafe_allow_html=True)
    # Sidebar for navigation
    st.sidebar.title("Choose a Roadmap")
    choice = st.sidebar.radio("Select an area", list(roadmap.keys()))

    # Centered header
    st.markdown(f"<h2 style='text-align: center;'>{choice} Roadmap</h2>", unsafe_allow_html=True)
    
    tech_stack = roadmap[choice]

    # Centered container for roadmap
    st.markdown("""
    <div style='text-align: center;'>
        <div style='display: flex; flex-direction: column; align-items: center;'>
    """, unsafe_allow_html=True)
    
    for i, tech in enumerate(tech_stack):
        # Create a button that, when clicked, displays course recommendations
        if st.button(tech, key=f"{choice}_{i}", help=f"Click to see courses for {tech}"):
            with st.expander(f"Recommended Courses for {tech}"):
                display_course_recommendations(tech)
        
        # Add a centered and larger arrow mark between the technologies
        if i < len(tech_stack) - 1:
            st.markdown(
                """
                <div style="margin: 20px 0;">
                    <span style="font-size: 48px;">&#8595;</span>
                </div>
                """, unsafe_allow_html=True
            )

    # Close the centered container
    st.markdown("</div></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    start()
