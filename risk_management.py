#Generate a risk management plan based on your project charter and save as an HTML file


import requests
import re
import markdown2


def fetch_deepseek_response(project_charter):

    DeepSeek_API_URL = "http://127.0.0.1:1234/v1/chat/completions"
    payload = {
        "model": "deepseek-r1-distill-qwen-7b",
        "messages": [ 
        { "role": "system", "content": "Act as IT Risk Analyst" },
        { "role": "user", "content": f"""
         Please generate a risk management plan based on my project charter : {project_charter}.
         Please provide me with a markdown output with clearly labelled headings and sub-headings.
            1. Risk Identification: Utilize SWOT Analysis to identify potential strengths, weaknesses, opportunities, and threats related to the project.
            Apply the Risk Assessment Matrix using Probability and Impact categories to systematically categorize identified risks.
            2. Documentation and Tools: Review existing project management templates to ensure all necessary inputs are addressed in risk identification and assessment.
            3. Risk Prioritization: Create a table with columns for Risk Name, Description, Probability, Impact, and Likely Cause. Assess the likelihood of each risk occurring and its potential impact on the project.
            4. Mitigation Strategies: Develop specific solutions or strategies for each identified risk, ensuring they are feasible within budget constraints and project limitations.
            5. Responsibility Assignment: Clearly assign responsibilities for implementing mitigation strategies to ensure accountability and effective management of risks.
            6. Risk Documentation: Maintain detailed records of all identified risks, their assessments, and the strategies in place. Ensure documentation is accessible to all stakeholders for understanding roles and project status updates.
            7. Regular Reviews: Conduct regular reviews of the risk management plan to keep it updated with any changes in project scope or environment.
            8. Impact Tracking: Track the actual impact of implemented risks post-strategy deployment to refine future approaches through continuous improvement.
            9. Dependency Consideration: Analyze interconnections among risks to address them comprehensively within the project context.
            10. External Influences: Engage external experts to assess risks arising from unpredictable factors like market changes or regulatory shifts.
            11. Communication: Ensure all stakeholders are informed about risk management processes, new risks, and progress in mitigation to foster collaboration and buy-in.
         
  
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
    risk_management_text = fetch_deepseek_response(project_charter)
    if risk_management_text:
        with open("risk_management.md", "w", encoding="utf-8") as file:
            file.write(risk_management_text)

        #conert markdown to html
        risk_management_html_txt = markdown2.markdown(risk_management_text, extras = ["fenced-code-blocks", "tables"])
        with open("risk_management.html", "w", encoding="utf-8") as file:
            file.write(risk_management_html_txt)
        print("Risk Management plan HTML File saved successfully ! ")
        return risk_management_text
    else:
        print("An unexpected error occured during risk management plan generation!")
        return None