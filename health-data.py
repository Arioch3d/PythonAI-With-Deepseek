#Medical Diagnosis: Create a Python Program that uses DeepSeek-R1 to analyze
#a patient's master health checkup report and gives them a breif report about their
#current health condition and suggest precautions to be taken.

import requests
import re


def fetch_deepseek_response(question):

    DeepSeek_API_URL = "http://127.0.0.1:1234/v1/chat/completions"
    payload = {
        "model": "deepseek-r1-distill-qwen-7b",
        "messages": [ 
        { "role": "system", "content": "Act as my Doctor." },
        { "role": "user", "content": question }
        ], 
        "temperature": 0.1, 
        "max_tokens": -1,
        "stream": False
    }
    #Step 3: Invoke the API and fetch response
    response = requests.post(DeepSeek_API_URL, json=payload)

    if response.status_code == 200:
        generated_response = response.json()
        answer = generated_response.get("choices")[0].get("message").get("content")
        filtered_answer = re.sub(r"<think>.*</think>", "",answer,flags=re.DOTALL).strip()
        return filtered_answer


CSV_File_Path = "HealthMetrics.csv"
try:
    with open(CSV_File_Path, "r") as file:
        csv_content = file.read()
except FileNotFoundError:
    print("Error: Missing File")

question = f"Analyze the below health data : {csv_content}. Please give me a health report and suggest any precautions I need to take."
answer = fetch_deepseek_response(question)
print(answer)
