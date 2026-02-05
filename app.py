# ... previous imports ...
# ... inside the "if submit ..." block ...

    try:
        genai.configure(api_key=api_key)
        
        # ⚠️ UPDATED MODEL NAME: gemini-1.5-flash -> gemini-2.0-flash
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"""
        Act as a Google Discover Specialist (2026).
        Headline: "{final_headline}"
        Topic: "{final_topic}"

        STRICT RULES:
        - Bullet points only.
        - Alternate headlines must be SENTENCE CASE.
        
        1. Score (1-10) with 1-sentence rationale:
           - Curiosity Gap
           - Entity Recognition
           - Trustworthiness
           - Discover Potential
        
        2. Provide 3 sentence-case alternates. Format:
           * [Headline] 
             - CTR: [X]% 
             - Why: [Reason]
        """
        
        with st.spinner("Analyzing..."):
            response = model.generate_content(prompt)
            st.subheader("Results")
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"API Error: {e}")
