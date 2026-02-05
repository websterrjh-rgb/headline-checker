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
    
    # Ensure this is all one statement
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content
