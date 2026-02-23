import os
from langchain_google_genai import ChatGoogleGenerativeAI

def get_llm():
    """Initializes and returns the Gemini LLM."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        raise ValueError("GEMINI_API_KEY environment variable is not set correctly.")
    
    # Using gemini-2.5-pro or gemini-2.5-flash for complex tasks
    # Ensure google-genai supports this model version
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        temperature=0.2, # Low temperature for more deterministic standard docs
        max_tokens=8192,
    )
    return llm
