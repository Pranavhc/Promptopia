import streamlit as st
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv; load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(
    page_title="Promptopia",
    layout="centered",
)

st.title("🚀 Promptopia")
st.subheader("Test your prompt engineering skills!")

user_prompt = st.text_area("Enter your prompt:", "", placeholder="The prompt is the text that the model uses to generate a response. Use the following controls over the hyperparameters of the Gemini 2.0 Flash LLM to customize the response. Good luck!")

# Hyperparameter Controls
temperature = st.slider("Temperature", 0.0, 2.0, 1.0, 0.01)
top_k = st.slider("Top-K Sampling", 0, 5000, 100, 1)
top_p = st.slider("Top-P (Nucleus Sampling)", 0.0, 1.0, 0.95, 0.01)
max_output_tokens = st.slider("Max Tokens", 1, 10000, 200, 1)

if st.button("Generate Response"):
    st.subheader("LLM Output")
    stream = st.empty()
    stream.write("Generating response... 🚀")
    full_response = ""

    if user_prompt.strip():
        response = client.models.generate_content_stream(
            model="gemini-2.0-flash",
            contents=user_prompt,
            config= types.GenerateContentConfig(
                max_output_tokens=max_output_tokens,
                temperature=temperature,
                top_k=top_k,
                top_p=top_p
            )
        )
        print(max_output_tokens, temperature, top_k, top_p)
        for chunk in response:
            if chunk.text: 
                full_response += chunk.text
                stream.write(full_response)
            else:
                stream.write("No response generated. Please try again.")
        
    else:
        st.warning("Please enter a prompt!")

st.markdown("---")
st.markdown("❤️ Made using Streamlit and Gemini 2.0 Flash")
