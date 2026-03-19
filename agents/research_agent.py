from crewai import Agent

def create_research_agent(llm):
    return Agent(
        role="Research Specialist",
        goal="Find accurate and useful information about the given topic",
        backstory="You are an expert researcher who gathers high-quality data.",
        llm=llm,
        max_retry_limit=1,
        verbose=True
    )