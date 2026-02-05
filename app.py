import streamlit as st
import requests
from bs4 import BeautifulSoup
from google import genai
from google.genai import types
from openai import OpenAI

# Page Configuration
st.set_page_config(page_title="PulseCheck 2026 | Multi-Model Analyzer", page_icon="📈")

# --- API KEY HANDLING ---
# Helper function to get key from secrets or sidebar
def get_api_key(service_name, secret_key):
    if secret_key in st.secrets:
        return st.secrets[secret_key]
    return None

# --- HELPER: WEB SCRAPER ---
def fetch_article_data(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.find('h1').get_text() if soup.find('h1') else (soup.find('title').get_text() if soup.find('title') else "No title found")
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        topic_hint = meta_desc['content'] if meta_desc else "General Content"
        
        return title.strip(), topic_hint.strip()
    except Exception as e:
        return None, str(e)

# --- HELPER: OPENAI CALL ---
def analyze_with_gpt(headline, topic, api_key):
    client = OpenAI(api_key=api_key)
    prompt = f"""
    Act as a Google Discover Specialist in 2026. Analyze this headline:
    HEADLINE: {headline}
    TOPIC: {topic}

    STRICT OUTPUT RULES:
    - Keep analysis short and punchy (bullet points).
    - Alternate headlines must be in **sentence case**.

    1. SCORECARD (1-10) with 1-sentence rationale:
       - Curiosity Gap
       - Entity Recognition
       - Trustworthiness (E-E-A-T)
       - Discover Potential

    2. OPTIMIZED ALTERNATES: 
       Provide 3 better headlines in sentence case.
       Format for EACH:
       * **[Headline Text]**
         - *Predicted CTR:* [Percentage]
         - *Why it wins:* [Explanation]
    """
    response =
