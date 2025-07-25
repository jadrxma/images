import streamlit as st
from openai import OpenAI
import base64

# Initialize OpenAI client with API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def encode_image_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode()

def analyze_image(image_bytes, question):
    base64_image = encode_image_to_base64(image_bytes)

    messages = [
        {"role": "system", "content": "You are an assistant that analyzes images and answers questions about them."},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": question},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content

st.title("Retail Stand Compliance Checker")

uploaded_file = st.file_uploader("Upload your retail stand image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, use_column_width=True)
    image_bytes = uploaded_file.read()
    if st.button("Analyze Stand Organization"):
        with st.spinner("Analyzing..."):
            question = "Is this retail display stand organized properly and compliant with merchandising standards?"
            result = analyze_image(image_bytes, question)
            st.subheader("Analysis Result")
            st.write(result)
