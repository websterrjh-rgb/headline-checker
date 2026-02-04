import streamlit as st
from google import genai
from google.genai import types

# Page Config
st.set_page_config(page_title="Discover ThinkTank 2026", page_icon="🧠")

# Sidebar for API Key
with st.sidebar:
    st.header("Authentication")
    api_key = st.text_input("Gemini API Key", type="password")
    st.info("Using Gemini 2.5 Flash with 'Thinking' enabled.")

st.title("🧠 Discover ThinkTank 2026")
st.write("Deep-reasoning analysis for Google Discover headlines.")

# Input Form
with st.form("think_form"):
    headline = st.text_input("Headline:", placeholder="Samsung Galaxy S26 vs iPhone 17...")
    url = st.text_input("URL:", placeholder="https://tech-news.com/article-123")
    topic = st.text_input("Primary Topic:", placeholder="Tech / Mobile")
    
    # New: Choose Thinking Intensity
    think_budget = st.select_slider(
        "Thinking Depth (Token Budget):",
        options=[0, 1024, 4096, 8192],
        value=4096,
        help="Higher budget = deeper analysis but slower response."
    )
    
    submit = st.form_submit_button("Analyze with Thinking Model", type="primary")

if submit:
    if not api_key:
        st.error("Please enter your API Key.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            
            prompt = f"""
            Analyze the following for Google Discover 2026 performance:
            Headline: {headline}
            URL: {url}
            Topic: {topic}

            CRITICAL INSTRUCTIONS:
            1. First, think deeply about the 2026 Google 'Interest Graph'. 
            2. Evaluate if the entities mentioned have high 'freshness' scores.
            3. Rate 1-10 on: Curiosity Gap, Entity Recognition, Trustworthiness, and Discover Potential.
            4. Provide 3 high-performing alternate headlines with their logic and scores.
            """

            with st.spinner("Model is 'thinking' through the strategy..."):
                # Call the model with thinking configuration
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        # Enabling the Thinking Model feature
                        thinking_config=types.ThinkingConfig(include_thoughts=True, budget_tokens=think_budget)
                    )
                )
                
                # Layout the Results
                st.success("Analysis Generated")

                # Display the Model's "Thoughts" in an expander
                if hasattr(response, 'thoughts'):
                    with st.expander("👁️ View Model's Internal Reasoning (Chain of Thought)"):
                        st.write(response.thoughts)

                st.divider()
                st.markdown(response.text)

        except Exception as e:
            st.error(f"Error: {e}")

st.divider()
st.caption("Optimized for 2026 Google Search & Discover Ecosystems.")