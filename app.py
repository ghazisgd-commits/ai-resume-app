import streamlit as st
import google.generativeai as genai
import PyPDF2

# --- Configuration ---
API_KEY = st.secrets.get("GEMINI_API_KEY") 
MODEL_NAME = 'gemini-2.0-flash' 

# --- Page Setup ---
st.set_page_config(page_title="Global AI Resume Builder", page_icon="🌍", layout="wide")

# --- Main App Interface ---
st.title("🌍 Global AI Resume & Cover Letter")
st.markdown("### دنیا کی کسی بھی زبان میں پروفیشنل CV اور لیٹر تیار کریں!")

# --- Language List (Top 25 Global Languages) ---
languages_list = [
    "English (International)", 
    "Urdu (اردو)", 
    "Roman Urdu",
    "Arabic (العربية)", 
    "Spanish (Español)", 
    "French (Français)", 
    "German (Deutsch)", 
    "Chinese (Simplified - 中文)",
    "Hindi (हिंदी)",
    "Russian (Русский)",
    "Portuguese (Português)",
    "Italian (Italiano)", 
    "Japanese (日本語)", 
    "Korean (한국어)",
    "Turkish (Türkçe)",
    "Indonesian (Bahasa Indonesia)",
    "Bengali (বাংলা)",
    "Persian (فارسی)",
    "Dutch (Nederlands)",
    "Polish (Polski)",
    "Thai (ไทย)",
    "Vietnamese (Tiếng Việt)"
]

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Settings / سیٹنگز")
    st.info("Choose your target language below:")
    
    # Language Dropdown
    language_option = st.selectbox(
        "Select Output Language:",
        languages_list
    )
    
    st.write(f"**Selected:** {language_option}")
    st.divider()
    st.caption("Powered by Gemini 2.0 Flash")

# --- Inputs ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Resume")
    uploaded_file = st.file_uploader("Upload PDF File", type="pdf")

with col2:
    st.subheader("2. Job Description")
    job_description = st.text_area("Paste job details here:", height=150)

# Function to extract text
def input_pdf_text(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += page.extract_text()
    return text

# --- Processing & Button ---
st.divider()

if st.button("Generate Smart Resume & Cover Letter 🚀", use_container_width=True):
    if not API_KEY:
        st.error("System Error: API Key is missing.")
    elif uploaded_file is None or not job_description:
        st.warning("⚠️ Please upload a resume and enter job description first.")
    else:
        with st.spinner(f"AI is thinking in {language_option}... Please wait..."):
            try:
                genai.configure(api_key=API_KEY)
                model = genai.GenerativeModel(MODEL_NAME)
                resume_text = input_pdf_text(uploaded_file)

                # --- The Magic Prompt ---
                input_prompt = f"""
                Act as a Global HR Consultant.
                
                Source Resume: {resume_text}
                Job Description: {job_description}
                Target Language: {language_option}
                
                Task:
                1. REWRITE the Resume Summary and Skills to perfectly match the Job Description keywords.
                2. WRITE a highly professional Cover Letter tailored to the company.
                
                IMPORTANT RULES:
                - The ENTIRE output must be in **{language_option}**.
                - If the language is Urdu/Arabic/Persian, ensure correct formatting.
                - Keep the tone professional and persuasive.
                
                Output Format: Markdown.
                """
                
                response = model.generate_content(input_prompt)
                
                # --- Success ---
                st.success("✅ Document Ready!")
                
                # --- Download Button Logic ---
                st.download_button(
                    label=f"📥 Download Result ({language_option})",
                    data=response.text,
                    file_name=f"Optimized_Resume_{language_option}.txt",
                    mime="text/plain",
                    type="primary" # Makes the button stand out
                )
                
                # --- Display Result ---
                st.subheader("Preview:")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")