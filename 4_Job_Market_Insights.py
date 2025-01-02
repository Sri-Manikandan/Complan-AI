import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(layout="wide")

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
    [data-testid="stSidebarContent"]{
        background-color: #304463; /* Bright button color */
        color: #ffffff; /* White text on buttons */
        
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

@st.cache_data
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error("File not found. Please check the file path.")
        return pd.DataFrame()

data = load_data(r'E:\Projects\Complan-AI\src\ai_job_market_insights.csv')

st.title("Future Job Market Insights")

# Main content layout with columns
col1, col2 = st.columns(2)

# Average Salary per Job Title
average_salary_per_job = data.groupby('Job_Title')['Salary_USD'].mean().reset_index()
average_salary_per_job = average_salary_per_job.sort_values(by='Salary_USD', ascending=False)

# Display average salary per job in a bar chart
fig_average_salary = px.bar(
    average_salary_per_job, 
    x='Job_Title', 
    y='Salary_USD', 
    title="Average Salary per Job Title",
    labels={'Salary_USD': 'Average Salary (USD)', 'Job_Title': 'Job Title'},
    text='Salary_USD'
)
fig_average_salary.update_traces(texttemplate='%{text:.2f}', textposition='outside')
col1.plotly_chart(fig_average_salary, use_container_width=True)

# Required Skills Pie Chart
skills_count = data['Required_Skills'].value_counts()
fig_skills = px.pie(
    values=skills_count.values,
    names=skills_count.index,
    title="Required Skills for the Jobs",
    hole=0.4
)
col2.plotly_chart(fig_skills, use_container_width=True)

# New row for Industry Insights
col3, col4 = st.columns(2)

# Jobs count by Industries using a Line Graph
industry_count = data['Industry'].value_counts().reset_index()
industry_count.columns = ['Industry', 'Count']
fig_industry = px.line(
    industry_count,
    x='Industry',
    y='Count',
    title="Job Count by Industry",
    labels={'Count': 'Job Count', 'Industry': 'Industry'}
)
fig_industry.update_traces(mode='lines+markers')
col3.plotly_chart(fig_industry, use_container_width=True)

# Required Skills vs AI Adoption Count Line Graph
adoption_skills_count = data.groupby(['Required_Skills', 'AI_Adoption_Level']).size().reset_index(name='Count')
fig_adoption_skills = px.line(
    adoption_skills_count,
    x='Required_Skills',
    y='Count',
    color='AI_Adoption_Level',
    title="Required Skills vs AI Adoption Count",
    labels={'Count': 'AI Adoption Count', 'Required_Skills': 'Required Skills'}
)
fig_adoption_skills.update_traces(mode='lines+markers')
col4.plotly_chart(fig_adoption_skills, use_container_width=True)

# Industry Job Growths
fig_growth = px.bar(
    data,
    x='Industry',
    y='Job_Growth_Projection',
    color='Job_Growth_Projection',
    title="Industry Job Growths",
    barmode='stack'
)
st.plotly_chart(fig_growth, use_container_width=True)
