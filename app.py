import streamlit as st
import google.generativeai as genai
import PyPDF2

# --- Configuration ---
# API Key is securely retrieved from Streamlit's Secrets and will be hidden from users.
API_KEY = st.secrets.get("GEMINI_API_KEY") 
MODEL_NAME = 'gemini-2.0-flash' 

# --- Page Setup ---
st.set_page_config(page_title="AI Resume Tailor", page_icon="🚀", layout="wide")

# --- Main App Interface ---
st.title("🚀 AI Resume & Cover Letter Generator")
st.markdown("### آپ کی نوکری کے مطابق CV اور کور لیٹر چند سیکنڈز میں تیار!")

st.info("💡 یہاں اپنے ریزیومے کی فائل اپلوڈ کریں اور مطلوبہ نوکری کی تفصیل (Job Description) پیسٹ کریں۔")

# 1. Upload PDF
uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

# 2. Job Description
job_description = st.text_area("Paste the Job Description (from the job posting) here:", height=200)

# Function to extract text from PDF
def input_pdf_text(uploaded_file):
    """Extracts text from the PDF file."""
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += page.extract_text()
    return text

# --- Button Logic ---
if st.button("Generate Optimized Resume and Cover Letter"):
    if not API_KEY:
        # This error should only appear if the key is missing from Streamlit Secrets
        st.error("Application Error: API Key is missing in the backend. Please contact the developer.")
    elif uploaded_file is None or not job_description:
        st.warning("Please upload a file and enter the job description to continue.")
    else:
        # Process started
        with st.spinner("AI is analyzing your profile and the job requirements..."):
            try:
                # 1. Configure AI
                genai.configure(api_key=API_KEY)
                model = genai.GenerativeModel(MODEL_NAME)
                
                # 2. Extract Text
                resume_text = input_pdf_text(uploaded_file)

                # 3. Prompt for Tailoring
                input_prompt = f"""
                Act as a professional HR Consultant specializing in ATS optimization.
                Resume Content: {resume_text}
                Job Description: {job_description}
                
                Task:
                1. Rewrite the Resume Summary and bullet points to maximize relevance to the Job Description (use direct keywords).
                2. Write a highly professional Cover Letter specifically tailored for this job.
                
                Output should be in clear Markdown format.
                """
                
                # 4. Generate Content
                response = model.generate_content(input_prompt)
                
                # 5. Show Result
                st.success("Analysis Complete!")
                st.subheader("Your Optimized Result:")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}. Check the API Key and try again with a smaller file.")