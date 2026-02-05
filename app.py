import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="PulseCheck 2026", page_icon="🧠")

# --- ⚠️ COMPLIANCE WARNING ---
st.warning("DO NOT USE HEADLINES VERBATIM. MODIFY PER AI CONTENT POLICY.", icon="⚠️")

# --- API KEY HANDLING ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    with st.sidebar:
        api_key = st.text_input("Enter Gemini API Key:", type="password")

# --- HELPER: WEB SCRAPER ---
def fetch_article_data(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Robust title extraction
        title = "No title found"
        if soup.find('h1'):
            title = soup.find('h1').get_text().strip()
        elif soup.title:
            title = soup.title.string.strip()
            
        return title
    except Exception as e:
        return None

# --- UI LAYOUT ---
st.title("🧠 PulseCheck 2026")
st.caption("Powered by Gemini 3.0 Thinking Model")

# Toggle between modes
input_mode = st.radio("Select Input Mode:", ["URL (Auto-Extract)", "Manual Headline"], horizontal=True)

# Initialize variables
final_headline = None
final_topic = None
trigger_analysis = False

# --- INPUT SECTION ---
with st.container(border=True):
    with st.form("analysis_form"):
        if input_mode == "URL (Auto-Extract)":
            url_input = st.text_input("Paste Article URL:")
            manual_headline = None
            manual_topic = None
        else:
            url_input = None
            manual_headline = st.text_input("Enter Headline:", placeholder="Type your headline here...")
            manual_topic = st.text_input("Topic (Optional):", placeholder="e.g. Tech")

        submitted = st.form_submit_button("Analyze with Gemini 3", type="primary", use_container_width=True)

    if submitted:
        if input_mode == "URL (Auto-Extract)" and url_input:
            with st.spinner("Scraping URL..."):
                extracted_title = fetch_article_data(url_input)
                if extracted_title:
                    st.success(f"Extracted: {extracted_title}")
                    final_headline = extracted_title
                    final_topic = "General"
                    trigger_analysis = True
                else:
                    st.error("Could not read URL. Try Manual Mode.")
        
        elif input_mode == "Manual Headline" and manual_headline:
            final_headline = manual_headline
            final_topic = manual_topic if manual_topic else "General"
            trigger_analysis = True
        
        else:
            st
