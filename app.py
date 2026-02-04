import streamlit as st
from google import genai
from google.genai import types

# Page Configuration
st.set_page_config(page_title="PulseCheck AI: Reasoning Engine", page_icon="🧠")

# --- API KEY HANDLING ---
# 1. Check Streamlit Secrets first (for cloud deployment)
# 2. Fallback to manual input if no secret is found
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    with st.sidebar:
        st.warning("No API Key found in secrets.")
        api_key = st.text_input("Enter Gemini API Key manually:", type="password")
        st.info("To avoid entering this every time, add it to your Streamlit Secrets.")

st.title("🧠 PulseCheck: Thinking Model")
st.write("Deep strategic analysis for Google Discover based on 2026 interest graphs.")

with st.form("analysis_form"):
    headline = st.text_input("Headline:", placeholder="e.g., iPhone 17 Pro vs S26 Ultra...")
    url = st.text_input("URL:", placeholder="https://example.com/...")
    topic = st.text_input("Primary Topic:", placeholder="e.g., Tech / Smartphones")
    
    submit_btn = st.form_submit_button("Analyze Headline", type="primary", use_container_width=True)

if submit_btn:
    if not api_key:
        st.error("Please provide an API Key to continue.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            
            prompt = f"""
            Analyze the following for Google Discover 2026 performance.
            URL: {url}

            Use deep reasoning to evaluate the 'Curiosity Gap,' 'Entity Recognition,' 'Trustworthiness,' and 'Discover Potential.' 
            Provide scores (1-10) and 3 high-performing alternate headlines with logic.
            """

            with st.spinner("Model is 'thinking' through the strategy..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        thinking_config=types.ThinkingConfig(include_thoughts=True)
                    )
                )
                
                # Show Feed Preview for context
                st.subheader("📱 Feed Preview Simulation")
                with st.container(border=True):
                    st.caption("Google Discover Card (2026 Layout)")
                    st.image("https://placehold.co/1200x630/202124/FFFFFF?text=Article+Hero+Image", use_container_width=True)
                    st.markdown(f"**{headline}**")
                    st.caption(f"{topic} • Just Now")

                if hasattr(response, 'thoughts'):
                    with st.expander("👁️ View Strategic Reasoning Process"):
                        st.markdown(response.thoughts)

                st.divider()
                st.markdown(response.text)

        except Exception as e:
            st.error(f"Analysis Error: {str(e)}")
