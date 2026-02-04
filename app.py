import streamlit as st
import requests
from bs4 import BeautifulSoup
from google import genai
from google.genai import types

# Page Configuration
st.set_page_config(page_title="PulseCheck 2026 | URL Analyzer", page_icon="🔗")

# --- API KEY HANDLING ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    with st.sidebar:
        st.warning("⚠️ API Key not found in secrets.")
        api_key = st.text_input("Enter Gemini API Key:", type="password")

# --- HELPER: WEB SCRAPER ---
def fetch_article_data(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract Title (Headline)
        title = soup.find('title').get_text() if soup.find('title') else "No title found"
        # Extract Meta Description as a proxy for Topic
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        topic_hint = meta_desc['content'] if meta_desc else "General Content"
        
        return title.strip(), topic_hint.strip()
    except Exception as e:
        return None, str(e)

# --- UI LAYOUT ---
st.title("🔗 PulseCheck 2026")
st.write("Enter a URL to analyze its Google Discover performance potential.")

url_input = st.text_input("Article URL:", placeholder="https://example.com/your-article")

if st.button("Fetch & Analyze", type="primary", use_container_width=True):
    if not api_key:
        st.error("Please provide an API Key.")
    elif not url_input:
        st.warning("Please enter a URL.")
    else:
        with st.spinner("🕵️ Scraping article and reasoning..."):
            headline, topic = fetch_article_data(url_input)
            
            if headline is None:
                st.error(f"Could not fetch data: {topic}")
            else:
                st.info(f"**Extracted Headline:** {headline}")
                
                try:
                    client = genai.Client(api_key=api_key)
                    
                    # Prompt specifically targeting your 4 pillars
                    prompt = f"""
                    System: Google Discover Algorithm Specialist (2026 Edition).
                    URL: {url_input}
                    Headline: {headline}
                    Context/Topic: {topic}

                    TASK:
                    1. Rate the headline from 1-10 on these 4 pillars:
                       - Curiosity Gap: Psychological pull without being clickbait.
                       - Entity Recognition: Presence of specific people/brands/products.
                       - Trustworthiness: E-E-A-T score & 2026 policy compliance.
                       - Discover Potential: Likelihood of viral feed placement.

                    2. Show your 'Thinking Log' for the 2026 Interest Graph.
                    3. Suggest 3 alternate headlines that score higher on ALL 4 scales.
                    4. Predict a CTR % for each version.
                    """

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            thinking_config=types.ThinkingConfig(include_thoughts=True)
                        )
                    )

                    # --- RESULTS DISPLAY ---
                    if hasattr(response, 'thoughts'):
                        with st.expander("👁️ View Algorithm Reasoning"):
                            st.markdown(response.thoughts)

                    st.subheader("📱 Feed Preview")
                    with st.container(border=True):
                        st.image("https://placehold.co/1200x630/202124/FFFFFF?text=Discover+Hero", use_container_width=True)
                        st.markdown(f"### {headline}")
                        st.caption(f"{topic[:100]}...")

                    st.divider()
                    st.markdown(response.text)

                except Exception as e:
                    st.error(f"AI Analysis Error: {e}")

st.markdown("---")
st.caption("PulseCheck 2026 | Automated URL Extraction + Gemini Reasoning")
