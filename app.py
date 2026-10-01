import os
import streamlit as st
from google import genai

st.set_page_config(
    page_title="AI Fashion Stylist",
    page_icon="👗",
    layout="centered"
)

st.title("👗 AI Fashion Stylist")
st.write(
    "Discover outfit combinations for your occasion "
    "with your personal AI fashion assistant!"
)

st.subheader("Tell us about your style")

clothes = st.text_input(
    "What clothes do you have?",
    placeholder="Example: Black kurti, blue jeans, white shirt"
)

occasion = st.selectbox(
    "Choose your occasion",
    [
        "College",
        "Casual outing",
        "Birthday party",
        "Wedding",
        "Festival",
        "Office",
        "Family function"
    ]
)

style = st.selectbox(
    "Choose your preferred style",
    [
        "Casual",
        "Traditional",
        "Indo-western",
        "Formal",
        "Party wear",
        "Minimal"
    ]
)

favorite_color = st.text_input(
    "Preferred colours (optional)",
    placeholder="Example: Black, pink, blue"
)

budget = st.selectbox(
    "Budget for additional items",
    [
        "No additional purchases",
        "Under ₹500",
        "₹500–₹1500",
        "Above ₹1500"
    ]
)

if st.button("✨ Suggest My Outfit", type="primary"):
    if not clothes.strip():
        st.warning("Please enter at least one clothing item.")
    else:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            st.error("Gemini API key is not configured.")
        else:
            client = genai.Client(api_key=api_key)

            prompt = f"""
You are a friendly AI Fashion Stylist.

Suggest practical outfit combinations using these preferences:

Available clothes: {clothes}
Occasion: {occasion}
Preferred style: {style}
Preferred colours: {favorite_color or "No preference"}
Budget for additional items: {budget}

Give the answer in simple English using these headings:
1. Recommended outfit
2. Colour combination
3. Footwear
4. Accessories
5. Optional additional items within budget
6. One alternative outfit

Prioritize clothing the user already owns.
Do not assume the user must buy anything.
Treat fashion preferences respectfully and avoid judging body shape.
"""

            try:
                with st.spinner("Creating your outfit suggestions..."):
                    response = client.models.generate_content(
                        model="gemini-3.1-flash-lite",
                        contents=prompt
                    )

                if response.text:
                    st.subheader("Your Personal Outfit Plan")
                    st.markdown(response.text)
                else:
                    st.warning("No suggestions were returned. Please try again.")

            except Exception as error:
                st.error(
                    "The AI request failed. Check your API key, "
                    "model availability, quota, and Render logs."
                )
                st.caption(str(error))
