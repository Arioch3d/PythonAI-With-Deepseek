'''
Build a pythong program that prompts the user for an app idea,
generates a project charter by hitting DeepSeek API.
Then, stores the returned results into a markdown file and word document.
'''

import requests
import re
from Markdown2docx import Markdown2docx


def fetch_deepseek_response(app_idea):

    DeepSeek_API_URL = "http://127.0.0.1:1234/v1/chat/completions"
    payload = {
        "model": "deepseek-r1-distill-qwen-7b",
        "messages": [ 
        { "role": "system", "content": "Act as a system architect" },
        { "role": "user", "content": f"""
         Generate a project charter for the following app idea " {app_idea}. Please include the following sections.
            1. Project Title: Clearly define the objective of the project, ensuring it is concise yet descriptive.
            2. Project Manager & Team: Identify the leader responsible for the project and list key team members contributing to its success.
            3. Project Objective: Articulate the goal or purpose of the project, specifying what the project aims to achieve.
            4. Deliverables: Enumerate all items, products, or services that will be produced as a result of the project.
            5. Gantt Chart/Timeline: Provide a timeline with key milestones and deliverable stages for clarity.
            6. Budget: Outline the financial details, including allocation by category to ensure transparency.
            7. Risk Management: List potential risks along with mitigation strategies to address them proactively.
            8. Quality Assurance: Describe methods or standards used to ensure the project meets required quality levels.
            9. Approval Levels & Signatures: Specify who requires prior approval for key decisions and provide signatures where applicable.
            10. Success Criteria: Define how success will be measured, allowing stakeholders to evaluate outcomes effectively.    
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


app_idea = input("Please enter your app idea:")
project_charter_text = fetch_deepseek_response(app_idea)
if project_charter_text:
    with open("project_charter.md", "w", encoding="utf-8") as file:
        file.write(project_charter_text)

    #convert md text to word document.
    word_file = Markdown2docx('project_charter')
    word_file.eat_soup()
    word_file.save()
    print("Project charter save successfully ! ")
else:
    print("An unexpected error occured during project charter generation!")