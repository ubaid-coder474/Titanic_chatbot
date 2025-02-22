import streamlit as st
import requests
import base64


st.title("Titanic Data Chatbot 🚢")

question = st.text_input("Ask a question about the Titanic dataset")

if st.button("Ask"):
    response = requests.get(f"http://127.0.0.1:8000/query/?question={question}").json()

    if response["response"]:
        st.write(response["response"])

    if response["image"]:
        image_bytes = base64.b64decode(response["image"])
        st.image(image_bytes, caption="Generated Visualization")
