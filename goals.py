class Goal:
    def __init__(self, question, visualization, rationale, index):
        self.question = question
        self.visualization = visualization
        self.rationale = rationale
        self.index = index

def goals_to_html(goals):
    html_goals = []
    for goal in goals:
        html_goal = f"""
        <h3 style="color:#D875C7">Goal {goal.index}</h3>
        <p style="font-size:30px; color:#E9A89B"><b>{goal.question}</b></p>
        <p style="font-size:20px"><b>Visualization:</b> {goal.visualization}</p>
        <p style="font-size:20px"><b>Rationale:</b> {goal.rationale}</p>
        """
        html_goals.append(html_goal)
    return html_goals
