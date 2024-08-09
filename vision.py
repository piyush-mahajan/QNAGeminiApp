from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API with the API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API key not found. Please set it in the .env file.")
    st.stop()

genai.configure(api_key=api_key)



# Function to get response from Gemini model based on user input and image
def get_gemini_response(input_text, image):
    model=genai.GenerativeModel('gemini-1.5-pro-001')
    try:
        if input_text:
            response = model.generate_content([input_text, image])
        else:
            response = model.generate_content(image)
        return response.text
    except Exception as e:
        st.error(f"Error fetching response from Gemini: {e}")
        return None

# Initialize the Streamlit app
st.set_page_config(page_title="Gemini Image Demo")
st.header("MahaGPT Plus Application")

# Input field for user prompt
input_text = st.text_input("Input Prompt: ", key="input")

# File uploader for image input
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = None

# Display the uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Button to submit the request
submit = st.button("Tell me about the image")

# If the submit button is clicked, get the response
if submit:
    if uploaded_file is not None:  # Check if the uploaded file is not None
        response = get_gemini_response(input_text, uploaded_file)  # Pass the uploaded file directly
        if response:
            st.subheader("The Response is")
            st.write(response)
    else:
        st.warning("Please upload an image before submitting.")