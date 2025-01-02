import tempfile
import requests
import streamlit as st
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (HRFlowable, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

st.set_page_config(page_title="Resume Builder", page_icon="🧠",layout="wide")
st.markdown(
    """
    <style>
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
    [data-testid="stSidebarContent"]{
        background-color: #304463; /* Bright button color */
        color: #ffffff; /* White text on buttons */
        
    }
.st-emotion-cache-6qob1r {
    position: relative;
    height: 100%;
    width: 100%;
    overflow: overlay;}
    /* Styling the hover effect on the navigation links */
    [data-testid="stSidebarNavLink"]:hover {
        background-color: #304463; /* Slightly lighter background on hover */
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
    /* App background */
    .stApp {
        background-color: #1e1e2f;
    }
    .stForm{
    width:700px;
    }
    /* Header styling */
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
        color: #ffffff;
    }
    
    /* Text input fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #2e2e3e;
        color: #ffffff;
        border: 1px solid #555555;
        border-radius: 5px;
    }
    
    /* Labels and headings */
    .stMarkdown, h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #ff6b6b;
        color: white;
        border-radius: 5px;
        height: 3em;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #ff4c4c;
    }
    
    /* Markdown text */
    .stMarkdown p {
        color: #ffffff;
    }
    
    /* Containers and other elements */
    .st-b7, .st-bc {
        background-color: #2e2e3e;
        color: #ffffff;
    }
    
    /* Form sections */
    .st-emotion-cache-qcpnpn {
        border: 2px solid #555555;
        border-radius: 10px;
        padding: 10px;
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
    """,
    unsafe_allow_html=True,
)



# Function to create the resume PDF
def create_resume_pdf(name, email, phone, address, education, experience, skills, hobbies, languages, leetcode_stats, github_stats):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        pdf_path = tmpfile.name

    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'TitleStyle', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=24, alignment=TA_CENTER
    )

    subtitle_style = ParagraphStyle(
        'SubtitleStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, spaceAfter=12, alignment=TA_LEFT
    )

    content_style = ParagraphStyle(
        'ContentStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=12, spaceAfter=10, leading=14
    )

    header_style = ParagraphStyle(
        'HeaderStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, spaceAfter=10, alignment=TA_CENTER
    )

    content = []
    content.append(Paragraph(name, title_style))
    content.append(Spacer(1, 6))
    contact_info = f"{email} &nbsp;&nbsp;|&nbsp;&nbsp; {phone}|&nbsp;&nbsp;{address}"
    contact_info = contact_info.replace("\n", ", ")
    contact_info = Paragraph(contact_info, header_style)
    content.append(contact_info)
    content.append(HRFlowable(width="100%", thickness=1, color="black"))
    content.append(Spacer(1, 12))

    def add_section(title, items, bullet=True):
        section = []
        section.append(Paragraph(title, subtitle_style))
        section.append(HRFlowable(width="40%", thickness=1, color="black", spaceAfter=6))
        for item in items:
            if bullet:
                section.append(Paragraph(f"• {item}", content_style))
            else:
                section.append(Paragraph(item, content_style))
        section.append(Spacer(1, 12))
        return section

    # Left half: Education, Work Experience, Hobbies
    left_column = []
    left_column.extend(add_section("Education", education, False))
    left_column.extend(add_section("Work Experience", experience, False))
    left_column.extend(add_section("Hobbies", hobbies))

    # Right half: Skills, GitHub Stats, LeetCode Stats, Languages
    right_column = []
    right_column.extend(add_section("Skills", skills))
    
    # GitHub Stats
    github_stats_section = [
        f"Total Repositories: {github_stats.get('total_repos', 'N/A')}",
        f"Primary Languages: {', '.join(github_stats.get('languages', []))}",
    ]
    right_column.extend(add_section("GitHub Stats", github_stats_section, False))
    
    # LeetCode Stats
    leetcode_stats_section = [
        f"Total Problems Solved: {leetcode_stats.get('totalSolved', 'N/A')}",
        f"Easy Problems Solved: {leetcode_stats.get('easySolved', 'N/A')} / {leetcode_stats.get('totalEasy', 'N/A')}",
        f"Medium Problems Solved: {leetcode_stats.get('mediumSolved', 'N/A')} / {leetcode_stats.get('totalMedium', 'N/A')}",
        f"Hard Problems Solved: {leetcode_stats.get('hardSolved', 'N/A')} / {leetcode_stats.get('totalHard', 'N/A')}",
    ]
    right_column.extend(add_section("LeetCode Stats", leetcode_stats_section, False))
    right_column.extend(add_section("Languages", languages))

    # Combine both columns into a table layout
    data = [[left_column, right_column]]

    table = Table(data, colWidths=[3.5 * inch, 3.5 * inch])
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))

    content.append(table)
    doc.build(content)

    return pdf_path

# Function to get LeetCode stats
def get_leetcode_stats(username: str):
    try:
        response = requests.get(f'https://leetcode-stats-api.herokuapp.com/{username}/')
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching LeetCode stats: {e}")
        return {"status": "error", "message": "Could not reach backend, try again later."}

# Function to get GitHub stats
def get_github_stats(username: str):
    try:
        response = requests.get(f'https://api.github.com/users/{username}/repos')
        repos = response.json()
        total_repos = len(repos)
        languages = set(repo['language'] for repo in repos if repo['language'])
        return {"total_repos": total_repos, "languages": list(languages)}
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching GitHub stats: {e}")
        return {"total_repos": 0, "languages": []}

# Main function to render the Streamlit UI
def main():
    st.title("Resume Builder")
    st.write("### Create a professional resume with ease.")

    with st.form(key='resume_form'):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Personal Information")
            name = st.text_input("Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            address = st.text_input("Address")

        with col2:
            st.subheader("Resume Details")
            
            education = st.text_area("Education (separate entries with a newline)", value="\n".join(st.session_state.get('education', [])))
            experience = st.text_area("Work Experience (separate entries with a newline)", value="\n".join(st.session_state.get('experience', [])))
            skills = st.text_area("Skills (separate entries with a newline)", value="\n".join(st.session_state.get('skills', [])))
            hobbies = st.text_area("Hobbies (separate entries with a newline)", value="\n".join(st.session_state.get('hobbies', [])))
            languages = st.text_area("Languages (separate entries with a newline)", value="\n".join(st.session_state.get('languages', [])))
            leetcode_username = st.text_input("LeetCode Username")
            github_username = st.text_input("GitHub Username")

            submit_button = st.form_submit_button("Generate PDF")
    
    if submit_button:
        if name and email and phone and address and education and experience and skills and hobbies and languages and leetcode_username and github_username:
            education_list = education.split('\n')
            experience_list = experience.split('\n')
            skills_list = skills.split('\n')
            hobbies_list = hobbies.split('\n')
            languages_list = languages.split('\n')

            leetcode_stats = get_leetcode_stats(leetcode_username)
            github_stats = get_github_stats(github_username)
            
            pdf_path = create_resume_pdf(
                name, email, phone, address,
                education_list, experience_list, skills_list,
                hobbies_list, languages_list, leetcode_stats, github_stats
            )
            
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
                st.download_button(label="Download Resume", data=pdf_bytes, file_name="resume.pdf", mime="application/pdf")
        else:
            st.error("Please fill out all fields before generating the resume.")

if __name__ == "__main__":
    main()
