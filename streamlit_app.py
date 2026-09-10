import streamlit as st
import base64
from groq import Groq
from PIL import Image
import io

st.set_page_config(page_title="Alpha Flora AI", page_icon="🌿", layout="centered")

st.title("🌿 Alpha Flora & Health AI")
st.write("Upload a photo of a plant, flower, or herb to identify it and check its health status.")

# Инициализация на Groq клиента
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

uploaded_file = st.file_uploader("Choose a plant image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    if st.button("Analyze Plant with AI"):
        with st.spinner("Analyzing plant health with Groq..."):
            try:
                # Конвертираме изображението в base64, за да го пратим към Groq API
                buffered = io.BytesIO()
                image.save(buffered, format=image.format if image.format else "JPEG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
                # Определяме типа на изображението
                img_format = image.format.lower() if image.format else "jpeg"
                if img_format == 'jpg':
                    img_format = 'jpeg'

                custom_prompt = (
                    "You are an expert botanist and plant pathologist. "
                    "Analyze this plant image and provide:\n"
                    "1. **Plant Name:** (Common and scientific name)\n"
                    "2. **Confidence:** (Estimated percentage)\n"
                    "3. **Health Status:** (Healthy or signs of disease/pests)\n"
                    "4. **Recommendation:** (Care or treatment advice)"
                )

                # Изпращаме заявката към топ безплатния визуален модел на Groq
                completion = client.chat.completions.create(
                    model="qwen/qwen3.6-27b",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": custom_prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/{img_format};base64,{img_str}"
                                    },
                                },
                            ],
                        }
                    ],
                    temperature=0.7,
                    max_tokens=700,
                )
                
                st.subheader("Analysis Results:")
                st.write(completion.choices[0].message.content)
                
            except Exception as e:
                st.error(f"Възникна грешка при анализа: {e}")