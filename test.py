import requests

url = "http://127.0.0.1:8000/upload/"
file_path = "GenAI.pdf"  # Replace with your PDF file


# with open(file_path, "rb") as file:
#     response = requests.post(url, files={"file": ("GenAI.pdf", file, "application/pdf")})
# print(response.json())



url = "http://127.0.0.1:8000/chat/"
response = requests.post(url, json={"question": "What are Generative AI Apps?"})
print(response.json())
