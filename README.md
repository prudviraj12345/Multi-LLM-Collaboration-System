# Multi-LLM Collaboration System

A simple multi-agent AI project built with CrewAI.

## Live Demo

Vercel URL:
https://vercelapp-ecru-omega.vercel.app

This project takes one user problem and solves it with 4 agents:
- Research Agent
- Coding Agent
- Review Agent
- Explanation Agent

You can run it in:
- Terminal mode (CLI)
- Browser mode (Streamlit UI)
- Live mode on Vercel (portfolio link)

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

For online deployment, we added a Vercel version with:
- Static frontend page
- Serverless API endpoint (`/api/run`)
- Same 4-agent step-by-step response format

Extra project points:
- Modular code structure (`agents/` and `tasks/`) for easy updates
- Supports multiple LLM providers using environment variables
- Beginner-friendly UI for non-technical users
- Can be deployed online and shared as a live portfolio project

---

## Tech Stack

- Python
- CrewAI
- Streamlit
- python-dotenv
- Node.js serverless API (for Vercel)
- Hugging Face API (or OpenAI API)
- Vercel

---

## Project Structure

```
MultiAgentLLM/
  agents/
  tasks/
  api/
  main.py
  web_app.py
  index.html
  vercel.json
  vercel_app/
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

Use Vercel:
1. Open `vercel_app` folder in terminal
2. Run `vercel --prod`
3. Add environment variables in Vercel project settings:
  - `LLM_PROVIDER`
  - `HUGGINGFACE_API_KEY` (or `OPENAI_API_KEY`)
  - `HUGGINGFACE_MODEL_NAME` (or `OPENAI_MODEL_NAME`)
4. Redeploy and use the generated live URL

---

## Notes

- Keep `.env` private
- Never push API keys to GitHub
- Rotate your key if exposed
