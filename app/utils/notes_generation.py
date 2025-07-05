import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_notes(keywords):
    try:
        if not keywords:
            raise ValueError("Keyword list is empty. Cannot generate notes.")

        gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not gemini_api_key:
            logger.error("Gemini API key not found")
            return "Gemini API key not found"

        print("📌 Received keywords:", keywords)
        print("🔐 API key present:", bool(gemini_api_key))

        genai.configure(api_key=gemini_api_key)

        keywords_string = ", ".join(keywords)

        system_prompt = """
        You are an intelligent note-generation assistant.
        Based on the given keywords, generate structured notes in the same language as keywords. Ensure the notes include the following sections:

        - **Title**: Clearly state the main topic.
        - **Pre-requisites**: Concepts or knowledge required to understand the notes.
        - **Introduction**: A brief overview of the topic.
        - **Simpler Analogy (Optional)**: Provide a simplified analogy for complex topics.
        - **Examples (Optional)**: Include examples to illustrate the topic.
        - **Relevant Formulas (Optional)**: List formulas related to the topic.
        - **Similar Topics**: Suggest related topics worth exploring.
        - **Summary**: Concise summary of the notes.

        Format the notes using Markdown syntax using appropriate heading styles.
        If any keyword is unfamiliar, explicitly state: "I don't have knowledge about this keyword."
        """

        query = f"{system_prompt}\nThese are the keywords: {keywords_string}"

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(query, stream=True)

        notes = []
        for chunk in response:
            print("🧠 Chunk received:", chunk.text)
            notes.append(chunk.text)

        full_notes = "\n".join(notes).strip()
        if not full_notes:
            raise RuntimeError("Failed to generate notes. Empty response.")

        return full_notes

    except Exception as e:
        logger.error(f"Error generating notes with Gemini API: {e}")
        raise
