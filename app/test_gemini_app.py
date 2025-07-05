import google.generativeai as genai

# Set your Gemini API key
genai.configure(api_key="GEMINI_API_KEY=AIzaSyBHXvzseMCJREIyXEw0M9rmyf5jdEba3eU")

# Create model instance
model = genai.GenerativeModel("gemini-1.5-flash")

# Generate content
response = model.generate_content("Hello, Gemini!")

print("Response:")
print(response.text)
