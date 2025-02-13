import streamlit as st
import google.generativeai as genai

# Streamlit App Title
st.title("⚡ AI Python Code Reviewer")

st.write("Submit your Python code for an automated review and receive a bug report with suggested fixes.")

# Configure Google Gemini AI API Key (Set in Streamlit Secrets for security)
API_KEY = st.secrets["GEMINI_API_KEY"]  # Store API key in Streamlit secrets
genai.configure(api_key=API_KEY)

# System Instruction for AI
sys_prompt = """You are an advanced Python code reviewer. Your task is to analyze the given Python code, identify potential bugs, logical errors, and areas of improvement, and suggest fixes.
                Your response should be structured as follows:
                1. **Issues Detected**: List any errors, inefficiencies, or improvements needed.
                2. **Fixed Code**: Provide the corrected version of the code.
                3. **Explanation**: Explain why the changes were made concisely.

                If the code is already optimal, acknowledge it and suggest best practices."""

# Function to review code
def code_review(code):
    """Sends user code to Google Gemini AI for review and handles responses."""
    try:
        model = genai.GenerativeModel("gemini-1.5-pro", system_instruction=sys_prompt)
        user_prompt = f"Review the following Python code and provide feedback on potential bugs, improvements, and fixes:\n\n```python\n{code}\n```"

        response = model.generate_content(user_prompt)

        return response.text.strip() if response.text else "No response received from AI."
    
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# User input section
code_input = st.text_area("Enter your Python code:", height=200, placeholder="Paste your Python code here...")

# Review button
if st.button("Review Code"):
    if code_input.strip():
        with st.spinner("Analyzing your code with Google AI..."):
            feedback = code_review(code_input)
        
        # Display output with proper formatting
        st.subheader("📋 Code Review Report")
        st.markdown(feedback)  # Display AI response with Markdown support
    else:
        st.warning("⚠️ Please enter some Python code before submitting.")
