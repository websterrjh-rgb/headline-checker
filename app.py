import streamlit as st
import requests
from bs4 import BeautifulSoup
from google import genai
from google.genai import types

# Page Configuration
st.set_page_config(page_title="PulseCheck 2026 | Discover Analyzer", page_icon="📈")

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
                    final_headline = fetched_title
                    final_topic = fetched_topic
                else:
                    st.error(f"Error fetching URL: {fetched_topic}")
    else:
        final_headline = st.text_input("Enter Headline:", placeholder="e.g., Why the S26 Ultra is the iPhone killer of 2026")
        final_topic = st.text_input("Topic/Category (Optional):", placeholder="e.g., Tech, Smartphones")

    submit_btn = st.button("Analyze for Discover", type="primary", use_container_width=True)

# --- ANALYSIS LOGIC ---
if submit_btn:
    if not api_key:
        st.error("Please provide an API Key.")
    elif not final_headline:
        st.warning("Please provide a headline or URL.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            
            # --- PROMPT WITH EXPLAINED RATINGS ---
            prompt = f"""
            Act as a Google Discover Specialist in 2026. 
            Analyze this content for the mobile 'Interest Feed' algorithm.

            HEADLINE: {final_headline}
            TOPIC: {final_topic}

            STRICT OUTPUT RULES:
            - Keep the analysis **short and punchy** (bullet points only, no fluff).
            - All suggested headlines must be in **sentence case** (only capitalize the first letter and proper nouns).

            1. SCORECARD (1-10) with 1-sentence rationale:
               - Curiosity Gap
               - Entity Recognition
               - Trustworthiness (E-E-A-T)
               - Discover Potential

            2. OPTIMIZED ALTERNATES: 
               Provide 3 better headlines in **sentence case**. 
               For EACH alternate, strictly follow this format:
               * **[Headline Text]**
                 - *Predicted CTR:* [Percentage]
                 - *Why it wins:* [Explain the specific psychological or algorithmic reason this scores higher than the original]
            """

            with st.spinner("🧠 Reasoning through Interest Graph..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        thinking_config=types.ThinkingConfig(include_thoughts=True)
                    )
                )

                # Thinking Expandable
                if hasattr(response, 'thoughts'):
                    with st.expander("👁️ View Strategic Reasoning"):
                        st.markdown(response.thoughts)

                # Feed Preview
                st.subheader("📱 Discover Feed Simulation")
                with st.container(border=True):
                    st.image("https://placehold.co/1200x630/202124/FFFFFF?text=Discover+Preview", use_container_width=True)
                    st.markdown(f"### {final_headline}")
                    st.caption(f"Source • {final_topic if final_topic else 'General'} • 2026 Algorithm")

                st.divider()
                st.markdown(response.text)

        except Exception as e:
            st.error(f"Analysis Error: {str(e)}")

st.markdown("---")
st.caption("PulseCheck 2026 | Powered by Gemini 2.5 Flash Thinking Model")
