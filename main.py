import project_charter
import risk_management
import project_plan


app_idea = input("Please enter your app idea:")
project_charter_text = project_charter.generate(app_idea)
risk_management.generate(project_charter_text)
project_plan.generate(project_charter_text)