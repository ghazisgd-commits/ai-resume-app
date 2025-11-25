import streamlit as st
import google.generativeai as genai
import PyPDF2

# --- Page Configuration ---
st.set_page_config(page_title="AI Resume App", page_icon="🚀")

# --- Sidebar ---
with st.sidebar:
    st.header("Settings")
    st.markdown("Get your API key from Google AI Studio")
    api_key = st.text_input("Enter Gemini API Key", type="password")

# --- Main App ---
st.title("🚀 AI Resume & Cover Letter Generator")
st.info("Tip: Upload a PDF (CV) and enter a Job Description.")

# 1. Upload PDF
uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

# 2. Job Description
job_description = st.text_area("Paste the Job Description here", height=200)

# Function to extract text from PDF
def input_pdf_text(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += page.extract_text()
    return text

# --- Button Logic ---
if st.button("Generate Resume"):
    if not api_key:
        st.error("Please enter your API Key first!")
    elif uploaded_file is not None and job_description:
        with st.spinner("AI (Gemini 2.0) is thinking..."):
            try:
                # 1. Configure API
                genai.configure(api_key=api_key)
                
                # 2. Select the Model (FROM YOUR LIST)
                model = genai.GenerativeModel('gemini-2.0-flash')
                
                # 3. Extract Text
                resume_text = input_pdf_text(uploaded_file)

                # 4. Create Prompt
                input_prompt = f"""
                Act as a professional HR Consultant.
                Resume Text: {resume_text}
                Job Description: {job_description}
                
                Task:
                1. Update the Resume Summary and Skills to match the Job Description.
                2. Write a highly professional Cover Letter.
                
                Output should be in Markdown format.
                """
                
                # 5. Generate Response
                response = model.generate_content(input_prompt)
                
                # 6. Show Result
                st.subheader("Here is your Optimized Result:")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please upload a file and enter a job description.")