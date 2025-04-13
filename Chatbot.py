#Build an AI-Powered Chatbot Using DeepSeek API
'''Develop a functional chatbot that:
    -Engages in Real-Time Conversations
    -Maintain context acress multiple conversation turns
    -Use 'exit' to end chat
'''
import requests
import re

def DeepSeek_chatbot():
    messages = [ 
            {"role": "system", "content": "Act as a friendly chatbot"}
        ]
    while True:    
        DeepSeek_API_URL = "http://127.0.0.1:1234/v1/chat/completions"
        question = input("You: ").strip()
        if question.lower() in ["exit", "quit"]:
            print("Goodbye! Great chatting with you")
            break
        messages.append({"role": "user", "content": question})
        payload = {
            "model": "deepseek-r1-distill-qwen-7b",
            "messages": messages,
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
            print("DeepSeek:",filtered_answer)
        
DeepSeek_chatbot()
