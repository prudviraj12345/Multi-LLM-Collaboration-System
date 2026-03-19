from crewai import Agent

def create_review_agent(llm):
    return Agent(
        role="Code Reviewer",
        goal="Review and improve the generated code",
        backstory="You are a senior developer ensuring code quality.",
        llm=llm,
        max_retry_limit=1,
        verbose=True
    )