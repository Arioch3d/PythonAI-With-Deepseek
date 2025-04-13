#Generate a risk management plan based on your project charter and save as an HTML file


import requests
import re
import markdown2
import table_to_excel
import table_to_pptx


def fetch_deepseek_response(project_charter):

    DeepSeek_API_URL = "http://127.0.0.1:1234/v1/chat/completions"
    payload = {
        "model": "deepseek-r1-distill-qwen-7b",
        "messages": [ 
        { "role": "system", "content": "Act as IT Risk Analyst" },
        { "role": "user", "content": f"""
         Please generate a robust project plan based on my project charter : {project_charter}.
         Please provide me with with a markdown table with columns such as Task Name, Duration, Dependencies, Status and Resources.
        """ }
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
    else:
        return None

def generate(project_charter):
    project_plan_text = fetch_deepseek_response(project_charter)
    print(project_plan_text)
    table_pattern = r"(\|.*\|(?:\n\|.*\|)*)"
    match = re.search(table_pattern, project_plan_text, re.DOTALL)
    project_plan_table = None
    if match:
        project_plan_table = match.group(0)
    else:
        print("No table found")
    if project_plan_table:
        with open("project_plan.md", "w", encoding="utf-8") as file:
            file.write(project_plan_table)
        
        table_to_excel.create_excel(project_plan_table, "project_plan")
        table_to_pptx.create_ppt(project_plan_table, "project_plan")
        print("Project Plan Successfully Generated.")

        return project_plan_table
    else:
        print("An unexpected error occured during risk management plan generation!")
        return None