import streamlit as st
from google import genai
from google.genai import types

# Page Configuration
st.set_page_config(page_title="PulseCheck 2026 | Discover Ranker", page_icon="📈")

# --- API KEY HANDLING (Streamlit Secrets) ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    with st.sidebar:
        st.warning("⚠️ No API Key found in secrets.")
        api_key = st.text_input("Enter Gemini API Key manually:", type="password")
        st.info("Add 'GEMINI_API_KEY' to your Streamlit Secrets to skip this.")

st.title("📈 PulseCheck 2026")
st.write("Rate and refine headlines for the Google Discover Interest Graph.")

# User Inputs
with st.container(border=True):
    headline = st.text_input("Current Headline:", placeholder="e.g., iPhone 17 Pro vs S26 Ultra...")
    url = st.text_input("Source URL (Optional):", placeholder="https://example.com/tech-news")
    topic = st.text_input("Primary Topic / Entities:", placeholder="e.g., Samsung Galaxy S26, Snapdragon 8 Gen 5")
    
    submit_btn = st.form_submit_button("Analyze & Rate", type="primary", use_container_width=True) if 'form' not in locals() else None
    # Note: Streamlit forms are best for multi-input, but for simplicity:
    submit_btn = st.button("Analyze & Rate", type="primary", use_container_width=True)

if submit_btn:
    if not api_key:
        st.error("Please provide an API Key.")
    elif not headline or not topic:
        st.warning("Headline and Topic are required for analysis.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            
            # The 2026 Strategy Prompt
            prompt = f"""
            System: Act as a Google Discover Algorithm Specialist (2026 Edition).
            Task: Analyze the following headline for the mobile 'Interest Feed'.
            
            Headline: {headline}
            URL: {url}
            Topic: {topic}

            1. Provide a score from 1-10 for:
               - Curiosity Gap: Psychological pull without being clickbait.
               - Entity Recognition: Presence of specific high-value people/brands/products.
               - Trustworthiness: E-E-A-T score & compliance with anti-clickbait policies.
               - Discover Potential: Likelihood of being featured in a user's feed.

            2. Provide a 'Thinking Log': Deeply reason through why this will or won't perform.
            3. Suggest 3 alternate headlines that score higher on ALL 4 scales while retaining factual accuracy. 
            4. Include a final 'Predicted CTR' for each suggestion.
            """

            with st.spinner("🧠 Gemini is reasoning through interest graph trends..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        thinking_config=types.ThinkingConfig(include_thoughts=True)
                    )
                )

                # --- UI DISPLAY ---
                st.success("Analysis Complete")

                # 1. Thinking Process (Expander)
                if hasattr(response, 'thoughts'):
                    with st.expander("👁️ View Algorithm Reasoning (Chain of Thought)"):
                        st.markdown(response.thoughts)

                # 2. Visual Feed Simulation
                st.subheader("📱 Feed Preview Simulation")
                with st.container(border=True):
                    st.image("https://placehold.co/1200x630/202124/FFFFFF?text=Article+Hero+Image", use_container_width=True)
                    st.markdown(f"### {headline}")
                    st.caption(f"Source • {topic} • 2026 Algorithm Approved")

                st.divider()

                # 3. Main Analysis Output
                st.markdown(response.text)

        except Exception as e:
            st.error(f"Error during analysis: {e}")

st.markdown("---")
st.caption("PulseCheck 2026 | Powered by Gemini 2.5 Flash Reasoning Engine")
