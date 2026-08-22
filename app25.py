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

# Your GitHub Personal Access Token
GITHUB_TOKEN = "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"

# Point the client to GitHub's free developer models endpoint
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=GITHUB_TOKEN.strip()
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
    You are an expert veterinary livestock appraiser. Analyze this livestock image thoroughly and produce a structured, high-accuracy assessment strictly in **{selected_lang}**.

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
                # Using GPT-4o-mini which has native vision and no strict veterinary censors
                completion = client.chat.completions.create(
                    model="gpt-4o-mini",
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