import streamlit as st
import google.generativeai as genai

st.title("🚀 AI Python Code Reviewer")
st.write("Submit your Python code for an automated review and receive a bug report with suggested fixes.")

API_KEY = st.secrets["general"]["API_KEY"]
if not API_KEY:
    st.error("⚠️ API Key not found. Please set it in `.streamlit/secrets.toml`.")
    st.stop()

genai.configure(api_key=API_KEY)

sys_prompt = """You are an advanced Python code reviewer. Your task is to analyze the given Python code, 
identify potential bugs, logical errors, and areas of improvement, and suggest fixes.
                
Response Format:
1. **Issues Detected**: List any errors, inefficiencies, or improvements needed.
2. **Fixed Code**: Provide the corrected version of the code.
3. **Explanation**: Explain why the changes were made concisely.

If the code is already optimal, acknowledge it and suggest best practices."""

def code_review(code):
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        user_prompt = f"Review the following Python code and provide feedback on potential bugs, improvements, and fixes:\n\n```python\n{code}\n```"

        response = model.generate_content(user_prompt)

        if response.text:
            return response.text.strip()
        else:
            return "⚠️ No response received from AI. Try again."
    
    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")
        return None

code_input = st.text_area("Enter your Python code:", height=200, placeholder="Paste your Python code here...")

 
if st.button("Review Code"):
    if code_input.strip():
        with st.spinner("Analyzing your code with Google AI..."):
            feedback = code_review(code_input)
        
        if feedback:
            st.subheader("📋 Code Review Report")
            st.markdown(feedback)  
    else:
        st.warning("⚠️ Please enter some Python code before submitting.")
st.markdown("---")  # Adds a separator line
st.markdown("👨‍💻 Made by **Yashwanth**")
