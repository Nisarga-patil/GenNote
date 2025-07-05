import os
import logging
import ast
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_keywords(extracted_text):
    try:
        if not extracted_text or not isinstance(extracted_text, str):
            raise ValueError("Invalid input: Extracted text is empty or not a string.")

        gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not gemini_api_key:
            logger.error("Gemini API key not found")
            return ["Gemini API key not found"]

        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
You are an intelligent keyword extraction model.
From the following input text, extract the **top 5–10 keywords** that represent the core topics.

Return ONLY a valid Python list of strings like:
['Computer Vision', 'Deep Learning', 'YOLO', 'Convolutional Networks']

Text:
{extracted_text}
"""

        response = model.generate_content(prompt)
        print("📤 Gemini raw response:\n", response.text)

        # Clean response if it’s wrapped in code block
        response_text = response.text.strip()
        if response_text.startswith("```"):
            response_text = response_text.split("\n", 1)[-1].rsplit("\n```", 1)[0]

        # Parse response as a Python list
        try:
            keywords = ast.literal_eval(response_text)
            if isinstance(keywords, list) and all(isinstance(k, str) for k in keywords):
                print("✅ Extracted keywords:", keywords)
                return keywords
            else:
                raise ValueError("Gemini returned invalid list structure.")
        except Exception as e:
            logger.error(f"❌ Failed to parse Gemini response:\n{response_text}")
            raise RuntimeError(f"Keyword extraction failed. Invalid format: {response_text}") from e

    except Exception as e:
        logger.error(f"❌ Error extracting keywords: {e}")
        raise
