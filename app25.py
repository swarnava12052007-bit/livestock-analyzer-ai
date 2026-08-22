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

# Your OpenRouter API Key
OPENROUTER_API_KEY = "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"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY.strip()
)

st.title("🐄 Smart Livestock Visual Analyzer")
st.write("Upload an image of cattle or buffalo to receive an exhaustive breed, sex, age stage, and complete veterinary profile breakdown.")

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

    # Resize image to optimize transmission
    image.thumbnail((700, 700))

    buffered = io.BytesIO()
    image.save(buffered, format="JPEG", quality=80)
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    image_url = f"data:image/jpeg;base64,{img_base64}"

    prompt = f"""
    You are a senior veterinary livestock specialist and animal geneticist. 
    Analyze this livestock image thoroughly and produce an exhaustive, multi-paragraph report strictly in **{selected_lang}**:

    1. **Taxonomy & Breed Authenticity:** (Identify species and specific breed such as Gir, Murrah, Sahiwal, Holstein Friesian, Nili-Ravi. Describe historical origins, purity markers, and typical regional lineage).
    2. **Sex & Reproductive Anatomy:** (Exhaustive breakdown of anatomical sex markers: udder conformation/teat placement, scrotal sac/sheath, neck crest musculature, and head profile).
    3. **Age & Physiological Maturation:** (Detailed age classification: Calf / Heifer-Young / Mature Adult with visual rationale based on body frame, skeletal maturity, and proportions).
    4. **Observed Phenotypic Traits:** (Detailed analysis of horn curvature, dorsal hump shape and placement, dewlap folds, skin pigmentation, and body condition score).
    5. **Economic Utility & Productivity Profile:** (Estimated daily milk yield potential or field traction capacity, climate adaptability, heat resilience, and parasite tolerance).
    6. **Veterinary Health & Feeding Protocol:** (Recommended daily feed formulation—dry roughage, green fodder, concentrate mix—plus routine vaccination milestones and diagnostic health screening markers).

    Provide thorough, multi-sentence explanations under every section with high technical precision. All headings and text must be in {selected_lang}.
    """

    if st.button("Analyze Full Profile", type="primary"):
        with st.spinner(f"Generating comprehensive veterinary report in {selected_lang}..."):
            # Reliable free vision models on OpenRouter
            models_to_try = [
                "google/gemma-3-27b-it:free",
                "qwen/qwen-2.5-vl-72b-instruct:free",
                "openrouter/free"
            ]
            
            response_content = None
            last_error = None

            for model_name in models_to_try:
                try:
                    completion = client.chat.completions.create(
                        model=model_name,
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
                        max_tokens=4096
                    )
                    response_content = completion.choices[0].message.content
                    break
                except Exception as e:
                    last_error = e
                    continue

            if response_content:
                st.markdown("---")
                st.markdown(f"### 📋 Veterinary & Breed Profile ({selected_lang})")
                st.markdown(response_content)
            else:
                st.error(f"Error analyzing image: {last_error}")