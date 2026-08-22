import base64
import io
from groq import Groq
from PIL import Image
import streamlit as st

st.set_page_config(
    page_title="Livestock Deep Analyzer", page_icon="🐄", layout="centered"
)

# Your Groq API Key
GROQ_API_KEY = (
    "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"
)
client = Groq(api_key=GROQ_API_KEY)

st.title("🐄 Smart Livestock Visual Analyzer")
st.write(
    "Upload an image of cattle or buffalo to receive a complete breed, sex,"
    " age stage, and profile breakdown."
)

uploaded_file = st.file_uploader(
    "Upload an image...", type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
  image = Image.open(uploaded_file).convert("RGB")
  st.image(image, caption="Target Animal", use_container_width=True)

  # Convert image to base64 data URL
  buffered = io.BytesIO()
  image.save(buffered, format="JPEG")
  img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
  image_url = f"data:image/jpeg;base64,{img_base64}"

  prompt = """
    You are an expert veterinary livestock specialist. Analyze this image thoroughly and provide a structured report:
    
    1. **Animal Type:** (Cattle / Buffalo / Other)
    2. **Identified Breed:** (e.g., Gir, Murrah, Sahiwal, Holstein Friesian, Nili-Ravi, etc.)
    3. **Estimated Sex:** (Male / Female — state visual cues such as udder/teats, muscular sheath, neck bulk, or horns)
    4. **Estimated Age Stage:** (Calf / Heifer-Young / Mature Adult — provide reasons based on body proportions)
    5. **Key Physical Traits Observed:** (Horn shape, hump presence, coat coloration, dewlap size)
    6. **Native Region & Primary Utility:** (Where this breed originates and whether it is Dairy, Draft, or Dual-purpose)
    
    Format the response clearly using clean markdown headings and bullet points.
    """

  if st.button("Analyze Full Profile", type="primary"):
    with st.spinner("Analyzing physical characteristics and breed markers..."):
      try:
        completion = client.chat.completions.create(
            model="qwen/qwen3.6-27b",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            }],
            temperature=0.2,
            max_tokens=1024,
        )
        st.markdown("---")
        st.markdown("### 📋 Veterinary & Breed Profile")
        st.markdown(completion.choices[0].message.content)
      except Exception as e:
        st.error(f"Error analyzing image: {e}")