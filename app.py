import streamlit as st
import requests
from bs4 import BeautifulSoup
from google import genai
from google.genai import types

# Page Configuration
st.set_page_config(page_title="PulseCheck 2026 | Discover Analyzer", page_icon="📈")

# --- ⚠️ COMPLIANCE WARNING ---
st.warning("DO NOT USE HEADLINES VERBATIM, PLEASE MODIFY THEM PER FUTURE'S AI CONTENT POLICY", icon="⚠️")

# --- API KEY HANDLING ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    with st.sidebar:
        st.warning("⚠️ No API Key found in secrets.")
        api_key = st.text_input("Enter Gemini API Key manually:", type="password")

# --- HELPER: WEB SCRAPER ---
def fetch_article_data(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract Headline and Description
        title = soup.find('h1').get_text() if soup.find('h1') else (soup.find('title').get_text() if soup.find('title') else "No title found")
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        topic_hint = meta_desc['content'] if meta_desc else "General Content"
        
        return title.strip(), topic_hint.strip()
    except Exception as e:
        return None, str(e)

# --- UI LAYOUT ---
st.title("📈 PulseCheck 2026")
st.write("Analyze headlines for Google Discover with AI-explained improvements.")

# Input Mode
input_mode = st.radio("Select Input Mode:", ["URL (Auto-Extract)", "Manual Headline"], horizontal=True)

final_headline = ""
final_topic = ""

with st.container(border=True):
    if input_mode == "URL (Auto-Extract)":
        url_input = st.text_input("Paste Article URL:", placeholder="https://techblog.com/new-iphone-rumors")
        if url_input:
            with st.spinner("Scraping article..."):
                fetched_title, fetched_topic = fetch_article_data(url_input)
                if fetched_title:
                    st.success(f"Extracted: **{fetched_title}**")
                    final_headline = fetched_
