import streamlit as st
import requests
import base64

st.title("Titanic Data Chatbot 🚢")

question = st.text_input("Ask a question about the Titanic dataset")

if st.button("Ask"):
    try:
        response = requests.get(
            "https://backend-oazo.onrender.com/",
            params={"question": question},
            timeout=10
        )

        st.write("Raw Response:", response.text)  # ✅ Print full response

        if response.status_code == 200:
            data = response.json()
            st.write("Parsed JSON:", data)  # ✅ Print parsed JSON

            if "response" in data and data["response"]:
                st.write(data["response"])

            if "image" in data and data["image"]:
                image_bytes = base64.b64decode(data["image"])
                st.image(image_bytes, caption="Generated Visualization")

        else:
            st.error(f"Error: Received status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")