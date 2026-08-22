import base64
import io
from PIL import Image
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Livestock Deep Analyzer",
    page_icon="🐄",
    layout="centered"
)

# Paste your Gemini AQ. API Key here
GEMINI_API_KEY = "AQ.Ab8RN6JU5FnS5IbbCQRLv-6y8gF2tcAnLkPkLYx0-uqXjGOhZA"

# Initialize the official Google GenAI client with headers for AQ keys
client = genai.Client(
    api_key=GEMINI_API_KEY.strip(),
    http_options=types.HttpOptions(headers={"x-goog-api-key": GEMINI_API_KEY.strip()})
)

st.title("🐄 Smart Livestock Visual Analyzer")
st.write("Upload an image of cattle or buffalo to receive an exhaustive species, breed, sex, age stage, and complete agricultural profile breakdown.")

# Multi-language selection dropdown
selected_lang = st.selectbox(
    "🌐 Select Report Language / भाषा चुनें",
    [
        "English",
        "Hindi (हिंदी)",
        "Punjabi (ਪੰਜਾਬੀ)",
        "Marathi (मराठी)",
        "Bengali (বাংলা)",
        "Gujarati (ગુજરાતી)",
        "Telugu (తెలుగు)",
        "Tamil (தமிழ்)"
    ],
    index=0
)

uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Target Animal", use_container_width=True)

    # Resize image to optimize transmission speed
    image.thumbnail((700, 700))

    prompt = f"""
    You are an expert agricultural livestock appraiser and animal nutritionist. 
    Analyze this livestock image thoroughly and produce a structured, high-accuracy assessment strictly in **{selected_lang}**.

    Provide direct, concise, and complete technical bullet points under each section:
    1. **Primary Species Identification:** (Explicitly determine first: Cattle vs Buffalo).
    2. **Taxonomy & Specific Breed:** (Identified breed such as Gir, Murrah, Sahiwal, etc.).
    3. **Sex & Anatomical Indicators:** (Visual cues like udder/teats, sheath, horn shape).
    4. **Age & Physiological Maturation:** (Calf / Young / Mature Adult).
    5. **Observed Phenotypic Traits:** (Horn curvature, dorsal hump, coat color).
    6. **Economic Utility & Productivity Profile:** (Estimated milk yield potential or draft capacity).
    7. **General Animal Husbandry & Nutritional Profile:** (Recommended daily diet formulation—roughage, green fodder, concentrate mix).

    Important Constraints:
    - Ensure EVERY numbered section from 1 to 7 is completely answered.
    - End the report with a final concluding sentence.
    """

    if st.button("Analyze Full Profile", type="primary"):
        with st.spinner(f"Generating complete agricultural report in {selected_lang}..."):
            try:
                # Using the active gemini-3.6-flash model
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=[image, prompt]
                )
                
                st.markdown("---")
                st.markdown(f"### 📋 Agricultural & Breed Profile ({selected_lang})")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error analyzing image: {e}")