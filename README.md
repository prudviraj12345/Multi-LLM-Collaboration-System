# Multi-LLM Collaboration System

A simple multi-agent AI project built with CrewAI.

This project takes one user problem and solves it with 4 agents:
- Research Agent
- Coding Agent
- Review Agent
- Explanation Agent

You can run it in:
- Terminal mode (CLI)
- Browser mode (Streamlit UI)

---

## What We Built

We created a Python project where multiple AI agents work step by step on the same request.

Flow:
1. Research agent finds approach
2. Coding agent writes solution
3. Review agent improves quality
4. Explanation agent gives simple final explanation

We also added a browser app to show:
- Each agent output
- Terminal logs
- Final combined output

---

## Tech Stack

- Python
- CrewAI
- Streamlit
- python-dotenv
- Hugging Face API (or OpenAI API)

---

## Project Structure

```
MultiAgentLLM/
  agents/
  tasks/
  main.py
  web_app.py
  requirements.txt
  .env
```

---

## Setup (First Time)

1. Open terminal in project folder
2. Create virtual environment
3. Install packages
4. Add API key in `.env`

### Commands

```powershell
cd C:\Users\USER\Desktop\MultiAgentLLM
python -m venv venv
& .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## Environment File

Create a `.env` file like this:

```env
LLM_PROVIDER=huggingface
HUGGINGFACE_API_KEY=your_key_here
HUGGINGFACE_MODEL_NAME=Qwen/Qwen2.5-7B-Instruct
```

For OpenAI:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key_here
OPENAI_MODEL_NAME=gpt-4o-mini
```

---

## Run in Terminal (CLI)

```powershell
cd C:\Users\USER\Desktop\MultiAgentLLM
& .\venv\Scripts\Activate.ps1
python main.py
```

---

## Run in Browser (Recommended)

```powershell
cd C:\Users\USER\Desktop\MultiAgentLLM
& .\venv\Scripts\Activate.ps1
streamlit run web_app.py --server.port 8501
```

Open:

http://localhost:8501

---

## Deploy Online (Live Link)

Use Streamlit Community Cloud:
1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Select repo and `web_app.py`
4. Add environment variables in Streamlit settings
5. Deploy and get your live URL

---

## Notes

- Keep `.env` private
- Never push API keys to GitHub
- Rotate your key if exposed

---

## Current Status

- Project pushed to GitHub
- Browser app added
- Agent-by-agent output visible in UI
- Ready for portfolio deployment
