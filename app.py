import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="PulseCheck Gemini 2026", page_icon="🪄")

# Sidebar for Gemini API Key
with st.sidebar:
    st.header("Authentication")
    api_key = st.text_input("Enter Gemini API Key", type="password", help="Get your key from Google AI Studio")
    st.info("Your key is processed only for this session.")
    st.markdown("[Get a Gemini API Key](https://aistudio.google.com/app/apikey)")

st.title("🪄 PulseCheck Gemini")
st.subheader("Google Discover 2026 Strategy Tool")

# Input Fields
with st.container(border=True):
    headline = st.text_input("Headline:", placeholder="e.g., iPhone 17 Pro vs S26 Ultra...")
    url = st.text_input("URL:", placeholder="https://tomsguide.com/...")
    topic = st.text_input("Primary Topic:", placeholder="e.g., Tech / Smartphones")
    
    analyze_btn = st.button("Generate Discover Analysis", type="primary", use_container_width=True)

# Application Logic
if analyze_btn:
    if not api_key:
        st.error("Missing Gemini API Key. Please provide one in the sidebar.")
    elif not headline or not topic:
        st.warning("Headline and Topic are required.")
    else:
        try:
            # Configure Gemini
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-pro') # Or 'gemini-1.5-flash' for speed
            
            prompt = f"""
            You are a Google Discover specialist in 2026. 
            Analyze this headline based on the 2026 'Interest Graph' and 'E-E-A-T' algorithm.

            Input Details:
            - Headline: {headline}
            - URL: {url}
            - Primary Topic: {topic}

            Tasks:
            1. Rate from 1-10 on:
               - Curiosity Gap (Psychological pull without being clickbait)
               - Entity Recognition (Presence of specific people/brands/products)
               - Trustworthiness (E-E-A-T score / Compliance with 2026 policies)
               - Discover Potential (Likelihood of being featured in the mobile feed)

            2. Provide a 'Strategic Verdict' (Why will this work or fail in 2026?).

            3. Provide 3 alternate headlines that score higher on all scales while maintaining 100% factual accuracy. 
               For each alternate, provide:
               - The Headline
               - A specific '2026 Alpha Reason' for why it's better
               - An Overall Discover Rating (0-100)
            """

            with st.spinner("Gemini is crunching the 2026 Feed Data..."):
                response = model.generate_content(prompt)
                
                # Layout for results
                st.success("Analysis Complete!")
                
                # Feed Preview Simulation
                st.subheader("📱 Feed Preview (2026 Mobile Simulation)")
                with st.container(border=True):
                    st.caption("Google Discover Card")
                    st.image("https://placehold.co/1200x630/202124/FFFFFF?text=Article+Hero+Image", use_container_width=True)
                    st.markdown(f"**{headline}**")
                    st.caption(f"{topic} • 2h ago")
                
                st.divider()
                st.markdown(response.text)

        except Exception as e:
            st.error(f"Analysis Error: {str(e)}")

st.markdown("---")
st.caption("PulseCheck 2026: Built for the Google Interest Graph.")