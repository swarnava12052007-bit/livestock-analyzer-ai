from PIL import Image
from google import genai
import streamlit as st

st.set_page_config(
    page_title="Livestock Deep Analyzer", page_icon="🐄", layout="centered"
)

# Your explicit API key
client = genai.Client(
    api_key="AQ.Ab8RN6JU5FnS5IbbCQRLv-6y8gF2tcAnLkPkLYxO-uqXjGOhZA"
)

st.title("🐄 Smart Livestock Visual Analyzer")
st.write(
    "Upload an image of a cattle or buffalo to receive a complete breed, sex,"
    " age stage, and profile breakdown."
)

uploaded_file = st.file_uploader(
    "Upload an image...", type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
  image = Image.open(uploaded_file)
  st.image(image, caption="Target Animal", use_container_width=True)

  prompt = """
    You are an expert veterinary livestock specialist. Analyze this image thoroughly and provide a structured report:
    
    1. **Animal Type:** (Cattle / Buffalo / Other)
    2. **Identified Breed:** (e.g., Gir, Murrah, Sahiwal, Holstein Friesian, Nili-Ravi, etc.)
    3. **Estimated Sex:** (Male / Female — state the visual cues such as udder/teats, muscular sheath, neck bulk, or horns)
    4. **Estimated Age Stage:** (Calf / Heifer-Young / Mature Adult — provide reasons based on body proportions)
    5. **Key Physical Traits Observed:** (Horn shape, hump presence, coat coloration, dewlap size)
    6. **Native Region & Primary Utility:** (Where this breed originates and whether it is Dairy, Draft, or Dual-purpose)
    
    Format the response clearly using clean markdown headings and bullet points.
    """

  if st.button("Analyze Full Profile", type="primary"):
    with st.spinner("Analyzing physical characteristics and breed markers..."):
      try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=[prompt, image]
        )
        st.markdown("---")
        st.markdown("### 📋 Veterinary & Breed Profile")
        st.markdown(response.text)
      except Exception as e:
        st.error(f"Error analyzing image: {e}")