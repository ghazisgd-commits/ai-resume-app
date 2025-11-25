import streamlit as st
import google.generativeai as genai
import PyPDF2

# --- Configuration ---
API_KEY = st.secrets.get("GEMINI_API_KEY") 
MODEL_NAME = 'gemini-2.0-flash' 

# --- Page Setup ---
st.set_page_config(page_title="Multilingual AI Resume", page_icon="🌍", layout="wide")

# --- Main App Interface ---
st.title("🌍 Multilingual AI Resume & Cover Letter")
st.markdown("### کسی بھی زبان میں CV اور کور لیٹر بنوائیں!")

# --- Sidebar for Options ---
with st.sidebar:
    st.header("⚙️ Settings")
    # Language Selection Dropdown
    language_option = st.selectbox(
        "Select Output Language / جواب کس زبان میں چاہیے؟",
        ("English", "Urdu (اردو)", "Roman Urdu", "Arabic (العربية)")
    )
    st.info(f"You selected: **{language_option}**")

st.info("💡 اپنا پرانا ریزیومے اپلوڈ کریں اور نوکری کی تفصیل پیسٹ کریں۔")

# 1. Upload PDF
uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

# 2. Job Description
job_description = st.text_area("Paste the Job Description here:", height=200)

# Function to extract text
def input_pdf_text(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += page.extract_text()
    return text

# --- Button Logic ---
if st.button("Generate Result / رزلٹ تیار کریں"):
    if not API_KEY:
        st.error("Error: API Key is missing.")
    elif uploaded_file is None or not job_description:
        st.warning("Please upload a file and enter description.")
    else:
        with st.spinner(f"AI is writing in {language_option}... Please wait..."):
            try:
                genai.configure(api_key=API_KEY)
                model = genai.GenerativeModel(MODEL_NAME)
                resume_text = input_pdf_text(uploaded_file)

                # --- The Magic Prompt (Updated for Language) ---
                input_prompt = f"""
                Act as a professional HR Consultant.
                Resume Content: {resume_text}
                Job Description: {job_description}
                Target Language: {language_option}
                
                Task:
                1. Update the Resume Summary and Skills matching the Job Description.
                2. Write a professional Cover Letter.
                
                IMPORTANT: Write the ENTIRE output (Resume and Cover Letter) strictly in **{language_option}** language.
                Output should be in Markdown format.
                """
                
                response = model.generate_content(input_prompt)
                
                st.success("Done!")
                st.subheader("Your Result:")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")