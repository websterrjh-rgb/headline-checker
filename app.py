import streamlit as st
from google import genai
from google.genai import types

# Page Configuration
st.set_page_config(page_title="PulseCheck AI: Strategic Thinking", page_icon="🧠")

# Sidebar for API Key
with st.sidebar:
    st.header("Authentication")
    api_key = st.text_input("Gemini API Key", type="password", help="Enter your Gemini 2.5 key")
    st.info("Now using 'Dynamic Thinking' for deep headline analysis.")

st.title("🧠 PulseCheck: Thinking Model")
st.write("Deep strategic analysis for Google Discover based on 2026 interest graphs.")

# Simple Input Form
with st.form("analysis_form"):
    headline = st.text_input("Headline:", placeholder="e.g., iPhone 17 Pro vs S26 Ultra...")
    url = st.text_input("URL:", placeholder="https://example.com/...")
    topic = st.text_input("Primary Topic:", placeholder="e.g., Tech / Smartphones")
    
    submit_btn = st.form_submit_button("Analyze Headline", type="primary", use_container_width=True)

# Application Logic
if submit_btn:
    if not api_key:
        st.error("Please provide an API Key in the sidebar.")
    elif not headline or not topic:
        st.warning("Please fill in both the Headline and Primary Topic.")
    else:
        try:
            # Initialize the 2026 GenAI Client
            client = genai.Client(api_key=api_key)
            
            # The prompt is optimized for a thinking-enabled model
            prompt = f"""
            Perform a deep-reasoning analysis for Google Discover performance.
            
            Headline: {headline}
            URL: {url}
            Topic: {topic}

            1. First, think about the current 2026 entity preferences and the 'Interest Graph' shifts.
            2. Rate from 1-10: Curiosity Gap, Entity Recognition, Trustworthiness, and Discover Potential.
            3. Provide a Strategic Verdict on the content's viability.
            4. Provide 3 high-performing alternate headlines with logic and a predicted score (0-100).
            """

            with st.spinner("Analyzing interest graphs..."):
                # Call Gemini 2.5 with Thinking Config
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        thinking_config=types.ThinkingConfig(
                            include_thoughts=True, # Shows the reasoning process
                            # thinking_budget removed as per request to use dynamic defaults
                        )
                    )
                )
                
                # Layout for results
                st.success("Strategic Analysis Complete")

                # Display the Model's Reasoning (The "Thinking" Part)
                if hasattr(response, 'thoughts'):
                    with st.expander("👁️ View Strategic Reasoning Process", expanded=False):
                        st.markdown(response.thoughts)

                st.divider()
                st.markdown(response.text)

        except Exception as e:
            st.error(f"Analysis Error: {str(e)}")

st.divider()
st.caption("PulseCheck 2026: Reasoning Engine Powered by Gemini 2.5.")
