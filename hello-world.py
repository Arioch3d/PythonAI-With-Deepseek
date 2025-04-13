#Invoke the DeepSeek local API using requests package and test out a few fun scenarios
import requests
import re
#Step 1: Find API URL - (server address + Endpoint)
DeepSeek_API_URL = "http://127.0.0.1:1234/v1/chat/completions"
#Step 2: Build request body/payload
question = input("Please ask your question ")
payload = {
    "model": "deepseek-r1-distill-qwen-7b",
    "messages": [ 
      { "role": "system", "content": "Always answer in rhymes." },
      { "role": "user", "content": question }
    ], 
    "temperature": 0.7, 
    "max_tokens": -1,
    "stream": False
  }
#Step 3: Invoke the API and fetch response
response = requests.post(DeepSeek_API_URL, json=payload)
#Step 4: Parse the API response to get answers.
if response.status_code == 200:
    generated_response = response.json()
    answer = generated_response.get("choices")[0].get("message").get("content")
    filtered_answer = re.sub(r"<think>.*</think>", "",answer,flags=re.DOTALL).strip()
    print(filtered_answer)