import google.generativeai as genai

genai.configure(api_key="AIzaSyDiL5wA12s7b6JYL2Nu4AuI94ov-I9xX0c")  # Your real key

model = genai.GenerativeModel(model_name="gemini-1.5-pro-001")
response = model.generate_content("Explain what a smurf attack is in one line.")
print("✅ Gemini Response:")
print(response.text)
