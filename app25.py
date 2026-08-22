import base64
import io
from groq import Groq
from PIL import Image
import streamlit as st

st.set_page_config(
    page_title="Livestock Deep Analyzer",
    page_icon="🐄",
    layout="centered"
)

# Your Groq API Key
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY.strip())

st.title("🐄 Smart Livestock Visual Analyzer")
st.write("Upload an image of cattle or buffalo to receive a complete breed, sex, age stage, and profile breakdown.")

# Language selection dropdown
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

    # Resize image to optimize token usage and stay within limits
    image.thumbnail((800, 800))

    buffered = io.BytesIO()
    image.save(buffered, format="JPEG", quality=85)
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    image_url = f"data:image/jpeg;base64,{img_base64}"

    prompt = f"""
    You are an expert veterinary livestock specialist and animal geneticist. 
    Thoroughly analyze this livestock image and produce a detailed report strictly in the chosen language: **{selected_lang}**.

    Ensure all section headers, technical details, and bullet points are written fluently in {selected_lang}:

    1. **Animal Classification & Breed:** (Cattle / Buffalo / Other, along with the precise breed such as Gir, Murrah, Sahiwal, Holstein Friesian, Nili-Ravi, etc.)
    2. **Estimated Sex & Anatomical Indicators:** (Male / Female — identify visual markers such as udder/teats, sheath, muscular neck bulk, or horn formation)
    3. **Estimated Age Stage & Frame:** (Calf / Heifer-Young / Mature Adult — evaluate body proportions, frame size, and growth markers)
    4. **Observed Phenotypic Traits:** (Horn curvature, presence/size of dorsal hump, coat color pattern, dewlap development)
    5. **Native Region & Primary Utility:** (Origin zone and whether it is specialized for Dairy, Draft, or Dual-purpose utility)
    6. **Care & Productivity Insights:** (Optimal feed suggestions, standard lactation/draft potential, and key health screening markers)

    Format clearly using bold titles, structured bullet points, and high technical accuracy.
    """

    if st.button("Analyze Full Profile", type="primary"):
        with st.spinner(f"Analyzing livestock markers in {selected_lang}..."):
            try:
                completion = client.chat.completions.create(
                    model="qwen/qwen3.6-27b",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": image_url
                                    }
                                }
                            ]
                        }
                    ],
                    temperature=0.2,
                    max_tokens=4096
                )
                st.markdown("---")
                st.markdown(f"### 📋 Veterinary & Breed Profile ({selected_lang})")
                st.markdown(completion.choices[0].message.content)
            except Exception as e:
                st.error(f"Error analyzing image: {e}")