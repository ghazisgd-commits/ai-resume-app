import streamlit as st
import google.generativeai as genai
import PyPDF2

# --- Configuration ---
API_KEY = st.secrets.get("GEMINI_API_KEY") 
MODEL_NAME = 'gemini-2.0-flash' 

# --- Page Setup (Wide Layout) ---
st.set_page_config(page_title="Pro AI Resume Builder", page_icon="💎", layout="wide")

# --- CUSTOM CSS (The Makeup) ---
# یہ حصہ آپ کی ایپ کو خوبصورت بناتا ہے
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(to right, #141e30, #243b55);
        color: white;
    }
    
    /* Input Fields Styling */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #2b3e50;
        color: white;
        border-radius: 10px;
        border: 1px solid #4a6985;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0b111a;
    }
    
    /* Custom Button Styling */
    div.stButton > button {
        background: linear-gradient(45deg, #FF512F 0%, #DD2476 51%, #FF512F 100%);
        color: white;
        padding: 15px 30px;
        text-align: center;
        text-transform: uppercase;
        transition: 0.5s;
        background-size: 200% auto;
        border-radius: 10px;
        border: none;
        font-weight: bold;
        width: 100%;
        box-shadow: 0 4px 15px 0 rgba(229, 66, 10, 0.75);
    }
    div.stButton > button:hover {
        background-position: right center; /* change the direction of the change here */
        color: #fff;
        text-decoration: none;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #f0f2f6;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Card Container */
    .css-1r6slb0 {
        background-color: #1e2a38;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown("<h1 style='text-align: center; color: #00d2ff;'>💎 Premium AI Resume Architect</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; color: #b0bec5;'>Crafted for Professionals. Powered by Gemini 2.0</p>", unsafe_allow_html=True)
st.divider()

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.markdown("## ⚙️ Control Panel")
    
    languages_list = [
        "English (Professional)", "Urdu (اردو)", "Arabic (العربية)", 
        "Spanish", "French", "German", "Chinese", "Hindi", "Russian"
    ]
    language_option = st.selectbox("Select Target Language:", languages_list)
    
    st.markdown("---")
    st.info("💡 **Pro Tip:** Paste the full job description for 95% ATS accuracy.")

# --- Main Interface (Two Columns Layout) ---
col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown("### 📂 Upload Your Resume")
    uploaded_file = st.file_uploader("", type="pdf", help="Upload your existing CV here")

with col2:
    st.markdown("### 📝 Job Description")
    job_description = st.text_area("", placeholder="Paste the job posting here...", height=200)

# Function
def input_pdf_text(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += page.extract_text()
    return text

# --- Processing Section ---
st.markdown("<br>", unsafe_allow_html=True) # Adding Space

if st.button("✨ GENERATE PREMIUM RESUME NOW ✨"):
    if not API_KEY:
        st.error("⚠️ API Key is missing! Check Secrets.")
    elif uploaded_file is None or not job_description:
        st.warning("⚠️ Please complete all fields above.")
    else:
        with st.spinner("🤖 AI is architecting your career profile..."):
            try:
                genai.configure(api_key=API_KEY)
                model = genai.GenerativeModel(MODEL_NAME)
                resume_text = input_pdf_text(uploaded_file)

                input_prompt = f"""
                Act as a Top-Tier Career Coach & HR Expert.
                Source Resume: {resume_text}
                Job Description: {job_description}
                Language: {language_option}
                
                Task:
                1. REWRITE the Executive Summary to be punchy and keyword-rich.
                2. OPTIMIZE Skills & Experience bullet points for high impact.
                3. WRITE a persuasive, high-converting Cover Letter.
                
                Format: Clean Markdown with bold headers.
                Language: Strictly {language_option}.
                """
                
                response = model.generate_content(input_prompt)
                
                # --- Success Display ---
                st.balloons() # Celebration effect
                st.success("✅ Success! Your documents are ready.")
                
                # Download Button
                st.download_button(
                    label="📥 DOWNLOAD FINAL DOCUMENT",
                    data=response.text,
                    file_name=f"Premium_Resume_{language_option}.txt",
                    mime="text/plain"
                )
                
                # Result Container
                with st.expander("📄 View Generated Content", expanded=True):
                    st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")