import streamlit as st
import requests
from bs4 import BeautifulSoup
from google import genai
from google.genai import types
from openai import OpenAI

# Page Configuration
st.set_page_config(page_title="PulseCheck 2026 | Multi-Model Analyzer", page_icon="📈")

# --- API KEY CONFIGURATION ---
# 1. OpenAI Key (Hardcoded as requested)
OPENAI_KEY = "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"

# 2. Gemini Key (From Secrets or Sidebar)
if "GEMINI_API_KEY" in st.secrets:
    gemini_key = st.secrets["GEMINI_API_KEY"]
else:
    gemini_key = None

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
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# --- HELPER: GEMINI CALL ---
def analyze_with_gemini(headline, topic, api_key):
    client = genai.Client(api_key=api_key)
    prompt = f"""
    Act as a Google Discover Specialist in 2026. 
    Analyze this content for the mobile 'Interest Feed' algorithm.

    HEADLINE: {headline}
    TOPIC: {topic}

    STRICT OUTPUT RULES:
    - Keep the analysis **short and punchy** (bullet points only).
    - All suggested headlines must be in **sentence case**.

    1. SCORECARD (1-10) with 1-sentence rationale:
       - Curiosity Gap
       - Entity Recognition
       - Trustworthiness (E-E-A-T)
       - Discover Potential

    2. OPTIMIZED ALTERNATES: 
       Provide 3 better headlines in **sentence case**. 
       For EACH, strictly follow this format:
       * **[Headline Text]**
         - *Predicted CTR:* [Percentage]
         - *Why it wins:* [Explain specific reason]
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(include_thoughts=True)
        )
    )
    return response

# --- UI LAYOUT ---
st.title("📈 PulseCheck 2026")
st.write("Analyze headlines for Google Discover using top-tier AI models.")

# Model Selector
model_choice = st.radio("Select AI Engine:", ["Gemini 2.5 Flash (Google)", "GPT-4o (OpenAI)"], horizontal=True)

# Input Toggle
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
                    final_headline = fetched_title
                    final_topic = fetched_topic
                else:
                    st.error(f"Error fetching URL: {fetched_topic}")
    else:
        final_headline = st.text_input("Enter Headline:", placeholder="e.g., Why the S26 Ultra is the iPhone killer")
        final_topic = st.text_input("Topic/Category (Optional):", placeholder="e.g., Tech, Smartphones")

    submit_btn = st.button(f"Analyze with {model_choice.split(' ')[0]}", type="primary", use_container_width=True)

# --- MAIN LOGIC ---
if submit_btn:
    if not final_headline:
        st.warning("Please provide a headline or URL.")
    else:
        try:
            # 1. GEMINI PATH
            if "Gemini" in model_choice:
                # Check for Gemini Key
                if not gemini_key:
                    with st.sidebar:
                        gemini_key = st.text_input("Gemini Key Required:", type="password")
                
                if not gemini_key:
                    st.error("Please provide a Gemini API Key to use this model.")
                else:
                    with st.spinner("🧠 Gemini is reasoning..."):
                        response = analyze_with_gemini(final_headline, final_topic, gemini_key)
                        
                        # Feed Preview
                        st.subheader("📱 Feed Preview")
                        with st.container(border=True):
                            st.image("https://placehold.co/1200x630/202124/FFFFFF?text=Discover+Preview", use_container_width=True)
                            st.markdown(f"### {final_headline}")
                            st.caption("Gemini 2.5 Analysis")

                        # Expandable Thinking (Gemini Exclusive)
                        if hasattr(response, 'thoughts'):
                            with st.expander("👁️ View Gemini's Strategic Reasoning"):
                                st.markdown(response.thoughts)
                        
                        st.divider()
                        st.markdown(response.text)

            # 2. GPT-4o PATH
            else:
                with st.spinner("🤖 GPT-4o is analyzing..."):
                    result_text = analyze_with_gpt(final_headline, final_topic, OPENAI_KEY)
                    
                    # Feed Preview
                    st.subheader("📱 Feed Preview")
                    with st.container(border=True):
                        st.image("https://placehold.co/1200x630/10a37f/FFFFFF?text=OpenAI+Preview", use_container_width=True)
                        st.markdown(f"### {final_headline}")
                        st.caption("GPT-4o Analysis")
                    
                    st.divider()
                    st.markdown(result_text)

        except Exception as e:
            st.error(f"Analysis Error: {str(e)}")

st.markdown("---")
st.caption("PulseCheck 2026 | Multi-Model Intelligence")
