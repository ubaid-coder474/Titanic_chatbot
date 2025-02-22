import streamlit as st
import requests
import base64

st.title("Titanic Data Chatbot 🚢")

question = st.text_input("Ask a question about the Titanic dataset")

if st.button("Ask"):
    if question.strip():  # Ensure the question is not empty
        try:
            response = requests.get("https://backend-oazo.onrender.com/", params={"question": question}).json()


            if response.status_code == 200:
                data = response.json()

                # Ensure "response" key exists in the JSON
                if "response" in data and data["response"]:
                    st.write(data["response"])
                else:
                    st.warning("No text response received from the backend.")

                # Ensure "image" key exists and is not empty
                if "image" in data and data["image"]:
                    try:
                        image_bytes = base64.b64decode(data["image"])
                        st.image(image_bytes, caption="Generated Visualization")
                    except Exception as e:
                        st.error(f"Failed to decode image: {e}")
                else:
                    st.warning("No image received from the backend.")

            else:
                st.error(f"Error {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to the backend: {e}")
    else:
        st.warning("Please enter a question before asking.")
