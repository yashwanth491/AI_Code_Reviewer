import streamlit as st
import google.generativeai as genai

# Streamlit App Title
st.title("⚡ AI Python Code Reviewer")

st.write("Submit your Python code for an automated review and receive a bug report with suggested fixes.")

# Configure Google Gemini AI API Key (Set in Streamlit Secrets for security)
API_KEY = st.secrets["GEMINI_API_KEY"]  # Store API key in Streamlit secrets
genai.configure(api_key=API_KEY)

# System Instruction for AI (Unchanged, but included for completeness)
sys_prompt = """You are an advanced Python code reviewer...""" # ... (rest of the prompt)

# Function to review code
def code_review(code):
    """Sends user code to Google Gemini AI for review and handles responses."""
    try:
        model = genai.GenerativeModel("gemini-1.5-pro", system_instruction=sys_prompt, temperature=0.1, top_p=0.5) # Added temperature and top_p
        user_prompt = f"Review the following Python code...\n\n```python\n{code}\n```"

        response = model.generate_content(user_prompt)

        return response.text.strip() if response.text else "No response received from AI."

    except genai.ApiException as e: # More specific exception handling
        return f"⚠️ Google AI API Error: {str(e)}"
    except Exception as e:  # Catch other potential errors
        return f"⚠️ An unexpected error occurred: {str(e)}"

# User input section
code_input = st.text_area("Enter your Python code:", height=200, placeholder="Paste your Python code here...")

# Review button
if st.button("Review Code"):
    if code_input.strip():
        try:
            compile(code_input, '<string>', 'exec') # Basic Python code validation
            with st.spinner("Analyzing your code with Google AI..."):
                feedback = code_review(code_input)

            # Display output with proper formatting
            st.subheader("📋 Code Review Report")
            st.code(feedback, language="markdown") # Display in a code block

        except SyntaxError as e:
             st.error(f"Invalid Python code: {e}")
    else:
        st.warning("⚠️ Please enter some Python code before submitting.")
