from crewai import Agent

def create_coding_agent(llm):
    return Agent(
        role="Code Generator",
        goal="Write clean and efficient code based on requirements",
        backstory="You are a skilled software engineer.",
        llm=llm,
        max_retry_limit=1,
        verbose=True
    )