import streamlit as st
import streamlit.components.v1 as components
from jinja2 import Template

def suggest_missing_skills(candidate_skills, required_skills):
    """
    Compares candidate skills with required skills (both comma-separated strings)
    and returns a list of missing skills.
    """
    # Convert comma-separated strings into lowercase sets
    candidate_set = set(skill.strip().lower() for skill in candidate_skills.split(",") if skill.strip())
    required_set = set(skill.strip().lower() for skill in required_skills.split(",") if skill.strip())
    
    # Missing skills are those in required_set but not in candidate_set
    missing = required_set - candidate_set
    return list(missing)

# Set page title
st.title("SmartResume Generator")

st.write("Fill in the details below to generate a customized resume and see which additional skills you might need.")

# --- Candidate Information ---
st.subheader("Candidate Information")
name = st.text_input("Name", "")
email = st.text_input("Email ID", "")
phone = st.text_input("Phone Number", "")
linkedin = st.text_input("LinkedIn (Optional)", "")

# --- Education Details ---
st.subheader("Education Details")
institution = st.text_input("Institution Name", "")
year_studied = st.text_input("Year(s) Studied (e.g., 2020-2024)", "")
percentage = st.text_input("Percentage (e.g., 80%)", "")

# --- Experience (Optional) ---
st.subheader("Experience (Optional)")
experience = st.text_area("Describe any work or internship experience here (leave blank if none).", "")

# --- Skills ---
st.subheader("Your Skills")
candidate_skills = st.text_input("List your skills (comma-separated)", "Python, Data Analysis")

# --- Job Details ---
st.subheader("Job/Company Description")
job_description = st.text_area("Describe the job or company here.", "We are looking for a data analyst to...")
required_skills = st.text_input("Required Skills for this Job (comma-separated)", "Python, SQL, Machine Learning")

# --- Generate Resume Button ---
if st.button("Generate Resume"):
    # Perform skill gap analysis
    missing_skills = suggest_missing_skills(candidate_skills, required_skills)
    
    # Jinja2 template for the resume
    template_str = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8"/>
        <title>{{ name }} - Resume</title>
        <style>
            body {
                font-family: Arial, sans-serif; 
                margin: 20px; 
                line-height: 1.6;
            }
            h1, h2 {
                color: #333; 
                margin-bottom: 5px;
            }
            .section {
                margin-bottom: 20px;
            }
            .section-title {
                font-size: 1.2em;
                font-weight: bold;
                border-bottom: 2px solid #333;
                margin-bottom: 10px;
            }
            .sub-section-title {
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <h1>{{ name }}</h1>
        <p>
          <strong>Email:</strong> {{ email }} | 
          <strong>Phone:</strong> {{ phone }}
          {% if linkedin %}| <strong>LinkedIn:</strong> {{ linkedin }}{% endif %}
        </p>
        
        <div class="section">
            <h2 class="section-title">Education</h2>
            <p class="sub-section-title">{{ institution }}</p>
            <p>Year(s) Studied: {{ year_studied }} | Percentage: {{ percentage }}</p>
        </div>
        
        {% if experience %}
        <div class="section">
            <h2 class="section-title">Experience</h2>
            <p>{{ experience }}</p>
        </div>
        {% endif %}
        
        <div class="section">
            <h2 class="section-title">Skills</h2>
            <p>{{ candidate_skills }}</p>
        </div>
        
        <div class="section">
            <h2 class="section-title">Job/Company Description</h2>
            <p>{{ job_description }}</p>
        </div>
        
        <div class="section">
            <h2 class="section-title">Suggested Skills to Consider</h2>
            {% if missing_skills %}
                <p>Based on the required skills, you might want to add or develop the following:</p>
                <ul>
                {% for skill in missing_skills %}
                    <li>{{ skill }}</li>
                {% endfor %}
                </ul>
            {% else %}
                <p>Your skills match the job requirements!</p>
            {% endif %}
        </div>
    </body>
    </html>
    """
    
    # Render the template
    template = Template(template_str)
    resume_html = template.render(
        name=name,
        email=email,
        phone=phone,
        linkedin=linkedin,
        institution=institution,
        year_studied=year_studied,
        percentage=percentage,
        experience=experience,
        candidate_skills=candidate_skills,
        job_description=job_description,
        missing_skills=missing_skills
    )
    
    # Display the fully styled HTML using st.components.v1.html
    st.write("### Resume Preview")
    components.html(resume_html, height=1000, scrolling=True)

