import os

from crewai import Crew, LLM
from dotenv import load_dotenv

# Import agents
from agents.research_agent import create_research_agent
from agents.coding_agent import create_coding_agent
from agents.review_agent import create_review_agent
from agents.explanation_agent import create_explanation_agent

# Import tasks
from tasks.tasks import create_tasks

# Load environment variables
load_dotenv(override=True)


def build_llm():
    provider = os.getenv("LLM_PROVIDER", "huggingface").strip().lower()

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini").strip()
        if not api_key:
            print("\nERROR: OPENAI_API_KEY is missing in .env.")
            print("Fix: add OPENAI_API_KEY=your_key in .env.")
            return None, provider

        return LLM(model=model_name, api_key=api_key), provider

    if provider == "huggingface":
        api_key = (os.getenv("HUGGINGFACE_API_KEY") or os.getenv("OPENAI_API_KEY") or "").strip()
        model_name = os.getenv("HUGGINGFACE_MODEL_NAME", "Qwen/Qwen2.5-7B-Instruct").strip()
        if not api_key:
            print("\nERROR: HUGGINGFACE_API_KEY is missing in .env.")
            print("Fix: add HUGGINGFACE_API_KEY=your_hf_key in .env.")
            return None, provider

        # CrewAI uses LiteLLM under the hood; huggingface/<repo_id> routes with HF token.
        return LLM(model=f"huggingface/{model_name}", api_key=api_key), provider

    print("\nERROR: Unsupported LLM_PROVIDER.")
    print("Use LLM_PROVIDER=openai or LLM_PROVIDER=huggingface in .env.")
    return None, provider


def main():
    llm, provider = build_llm()
    if llm is None:
        return

    user_problem = input("Enter your problem or request: ").strip()
    if not user_problem:
        print("ERROR: Please enter a valid problem statement.")
        return

    # Create agents
    research_agent = create_research_agent(llm)
    coding_agent = create_coding_agent(llm)
    review_agent = create_review_agent(llm)
    explanation_agent = create_explanation_agent(llm)

    # Create tasks
    tasks = create_tasks(
        research_agent,
        coding_agent,
        review_agent,
        explanation_agent,
        user_problem
    )

    # Create crew
    crew = Crew(
        agents=[research_agent, coding_agent, review_agent, explanation_agent],
        tasks=tasks,
        verbose=True
    )

    # Run crew
    try:
        result = crew.kickoff()
    except Exception as exc:
        error_text = str(exc).lower()
        if "insufficient_quota" in error_text or "exceeded your current quota" in error_text:
            print(f"\nERROR: {provider} quota exceeded.")
            print("Fix: add billing/credits for the selected provider key in .env.")
            return
        if "invalid_api_key" in error_text or "incorrect api key" in error_text or "401" in error_text:
            print(f"\nERROR: Invalid {provider} API key.")
            print("Fix: update the provider key in .env and retry.")
            return
        raise

    print("\n\n FINAL OUTPUT:\n")
    print(result)


if __name__ == "__main__":
    main()