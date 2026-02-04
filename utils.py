import os
import fitz  # PyMuPDF
import google.generativeai as genai
from dotenv import load_dotenv
import json
import re

# Load environment variables
load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def extract_text(uploaded_file):
    """
    Extracts text from an uploaded PDF file using PyMuPDF.
    """
    try:
        # Read file bytes
        file_bytes = uploaded_file.read()
        
        # Open PDF from bytes
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        
        text = ""
        for page in doc:
            text += page.get_text()
            
        return text
    except Exception as e:
        return f"Error extracting text: {e}"

def clean_text(text):
    """
    Cleans raw text by removing headers, footers, and excessive whitespace.
    """
    # Remove multiple newlines
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    # Remove page numbers (heuristic: simple digits on a line)
    text = re.sub(r'\n\d+\n', '\n', text)
    
    # Remove whitespace artifacts
    text = text.strip()
    
    return text

def chunk_text(text, chunk_size=2000):
    """
    Splits text into logical blocks (clauses/paragraphs).
    Simple implementation: split by paragraphs and group them.
    """
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        if len(current_chunk) + len(para) > chunk_size:
            chunks.append(current_chunk)
            current_chunk = para
        else:
            current_chunk += "\n\n" + para
            
    if current_chunk:
        chunks.append(current_chunk)
        
    return chunks

def analyze_with_gemini(text_chunk, contract_type="General"):
    """
    Sends text to Gemini for risk analysis.
    """
    if not api_key:
        return {"error": "API Key not found."}

    # List of models to try in order of preference
    models_to_try = [
        'gemini-2.5-flash',
        'gemini-2.0-flash',
        'gemini-2.5-pro',
        'gemini-2.0-flash-lite',
        'gemini-pro'
    ]

    prompt = f"""
    You are a legal expert AI. Analyze the following text from a {contract_type} contract.
    Identify any potential risks, clauses that are ambiguous, or terms that are unfavorable to the signer.
    
    Output the result STRICTLY as a JSON object with the following structure:
    {{
        "risks": [
            {{
                "category": "High" | "Medium" | "Low",
                "risk_type": "Short title of the risk",
                "explanation": "Detailed explanation of why this is risky.",
                "quote": "The exact substring from the text that triggers this risk."
            }}
        ]
    }}
    
    If no risks are found, return {{"risks": []}}.
    
    Text to analyze:
    {text_chunk}
    """

    last_error = None
    
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            return json.loads(response.text)
        except Exception as e:
            last_error = e
            continue  # Try next model
            
    # If all models fail
    return {"error": f"All models failed. Last error: {str(last_error)}", "risks": []}

def verify_quotes(risks_data, original_text):
    """
    Verifies if the quotes in the risk assessment actually exist in the original text.
    """
    verified_risks = []
    
    if "risks" not in risks_data:
        return risks_data

    for risk in risks_data["risks"]:
        quote = risk.get("quote", "")
        # Normalize whitespace for comparison
        normalized_quote = " ".join(quote.split())
        normalized_text = " ".join(original_text.split())
        
        if normalized_quote in normalized_text:
            risk["verified"] = True
        else:
            risk["verified"] = False
            
        verified_risks.append(risk)
        
    return {"risks": verified_risks}
