from crewai import Agent

def create_explanation_agent(llm):
    return Agent(
        role="Explainer",
        goal="Explain the solution in simple terms",
        backstory="You are a great teacher who simplifies concepts.",
        llm=llm,
        max_retry_limit=1,
        verbose=True
    )