import base64
import io
from PIL import Image
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Livestock Deep Analyzer",
    page_icon="🐄",
    layout="centered"
)

# Paste your NVIDIA API Key here (starts with nvapi-)
NVIDIA_API_KEY = "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"

# Point the client to NVIDIA's OpenAI-compatible endpoint
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY.strip()
)

st.title("🐄 Smart Livestock Visual Analyzer")
st.write("Upload an image of cattle or buffalo to receive an exhaustive species, breed, sex, age stage, and complete veterinary profile breakdown.")

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

    buffered = io.BytesIO()
    image.save(buffered, format="JPEG", quality=80)
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    # Standard Base64 data URI format
    image_url = f"data:image/jpeg;base64,{img_base64}"

    prompt = f"""
    You are a senior veterinary livestock specialist and animal geneticist. 
    Analyze this livestock image thoroughly and produce a structured, high-accuracy assessment strictly in **{selected_lang}**.

    Provide direct, concise, and complete technical bullet points under each section:

    1. **Primary Species Identification:** (Explicitly determine first: **Cattle (गाय / Bovine)** vs **Buffalo (भैंस / Bubaline)** with key anatomical distinctions like horn orientation, muzzle shape, skin texture, and dewlap structure).
    2. **Taxonomy & Specific Breed:** (Identified breed such as Gir, Murrah, Sahiwal, Holstein Friesian, Nili-Ravi, etc., along with regional origin and purity indicators).
    3. **Sex & Anatomical Indicators:** (Sex identification with key visual cues: udder/teats, sheath, musculature, horn shape).
    4. **Age & Physiological Maturation:** (Classification: Calf / Young / Mature Adult with visual markers based on body frame and proportions).
    5. **Observed Phenotypic Traits:** (Analysis of horn curvature, dorsal hump presence, dewlap folds, coat color).
    6. **Economic Utility & Productivity Profile:** (Estimated milk yield potential or draft capacity, heat resilience, and climate adaptability).
    7. **Veterinary Health & Feeding Protocol:** (Recommended feed formulation—roughage, green fodder, concentrate mix—and key health screening markers).

    Important Constraints:
    - Ensure EVERY numbered section from 1 to 7 is completely answered.
    - Keep explanations high-signal and structured so the report finishes smoothly.
    - End the report with a final concluding sentence.
    """

    if st.button("Analyze Full Profile", type="primary"):
        with st.spinner(f"Generating complete veterinary report in {selected_lang}..."):
            try:
                # Using NVIDIA's hosted Llama 3.2 11B Vision model
                completion = client.chat.completions.create(
                    model="meta/llama-3.2-11b-vision-instruct",
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
                    max_tokens=3000
                )
                
                st.markdown("---")
                st.markdown(f"### 📋 Veterinary & Breed Profile ({selected_lang})")
                st.markdown(completion.choices[0].message.content)
                
            except Exception as e:
                st.error(f"Error analyzing image: {e}")