import google.generativeai as genai

# Use your valid Gemini API key
genai.configure(api_key="AIzaSyCknY9Y7h7xnAXXpLIpUnjh7KLD4jY8LG4")

def test_gemini():
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Hello Gemini! Can you explain AI in one sentence?")
        print("✅ Gemini replied:\n")
        print(response.text)
    except Exception as e:
        print("❌ Error while calling Gemini:", e)

test_gemini()

