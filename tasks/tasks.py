from crewai import Task

def create_tasks(research_agent, coding_agent, review_agent, explanation_agent, user_problem):

    research_task = Task(
        description=f"Research and gather information to solve this user request: {user_problem}",
        agent=research_agent,
        expected_output="Detailed explanation and approach"
    )

    coding_task = Task(
        description=f"Write code to solve the user's request: {user_problem}",
        agent=coding_agent,
        expected_output="Working Python code"
    )

    review_task = Task(
        description=f"Review and improve the solution for this request: {user_problem}",
        agent=review_agent,
        expected_output="Improved and optimized code"
    )

    explanation_task = Task(
        description=f"Explain the final solution for this request in simple terms: {user_problem}",
        agent=explanation_agent,
        expected_output="Beginner-friendly explanation"
    )

    return [research_task, coding_task, review_task, explanation_task]