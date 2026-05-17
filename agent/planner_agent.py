def plan_task(user_input):

    user_input = user_input.lower()

    if "optimize" in user_input or "improve" in user_input:
        return [
            ("cleanup", "Clean Python cache folders"),
            ("structure", "Create logs folder"),
            ("report", "Show project structure")
        ]

    return []