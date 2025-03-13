import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Promptopia",
    layout="centered",
)

st.title("🚀 Promptopia")
st.subheader("Test your prompt engineering skills!")

# Get the Gemini API Key from the user.
user_api_key: str = st.text_input(
    "Enter your Gemini API Key:",
    placeholder="You cannot proceed without a valid API key",
    type="password"
)

if user_api_key:
    try:
        client = genai.Client(api_key=user_api_key)
        
        user_prompt: str = st.text_area("Enter your prompt:", "", placeholder="Enter your prompt (max 70 tokens)")
        
        # Approximate token count using whitespace splitting.
        token_count = len(user_prompt.split())
        st.write(f"Token count: {token_count}")
        
        if token_count > 70:
            st.error("Your prompt exceeds the 70 token limit. Please shorten your prompt.")
        else:
            if st.button("Generate Response"):
                st.subheader("LLM Output")
                stream = st.empty()
                stream.write("Generating response... 🚀")
                full_response = ""
                
                if user_prompt.strip():
                    response = client.models.generate_content_stream(
                        model="gemini-2.0-flash",
                        contents=user_prompt,
                        config=types.GenerateContentConfig(
                            temperature=0.01,
                            top_k=100,
                            top_p=0.95
                        )
                    )
                    for chunk in response:
                        if chunk.text: 
                            full_response += chunk.text
                            stream.write(full_response)
                        else:
                            stream.write("No response generated. Please try again.")
                else:
                    st.warning("Please enter a prompt!")
    except Exception as e:
        st.error("Invalid API Key. Please try again.")
else:
    st.warning("Please contact your co-ordinator for support.")

st.markdown("---")
st.markdown("❤️ Made at DESPU for PROMPTOPIA.")
