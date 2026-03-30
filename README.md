[project]
name = "code-review-env"
version = "1.0.0"
description = "AI Code Review Environment using FastAPI and OpenEnv"
authors = [
    { name = "Kavin Kaarthik" }
]
readme = "README.md"
requires-python = ">=3.8"

dependencies = [
    "fastapi",
    "uvicorn",
    "pydantic",
    "httpx",
    "python-dotenv"
]

[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"





📘 Code Review Environment (OpenEnv Compatible)
🚀 Overview
This project implements a Code Review Environment where an agent (or user) analyzes code, identifies issues, and submits fixes. The environment evaluates the review and assigns a score based on correctness.
It is designed to simulate a reinforcement learning / agent-based code review system.
---
🎯 Features
🔍 Detects issues in code (syntax, logic, best practices)
🛠 Accepts corrected code submissions
📊 Provides scoring based on:
Issue detection accuracy
Code fix similarity
🔁 Step-based interaction (like an RL environment)
🌐 REST API + WebSocket support (FastAPI)
⚡ Multiple predefined tasks
---
🧱 Project Structure
```
code_review_env/
│
├── server/
│   ├── app.py              # FastAPI server
│   ├── environment.py      # Core environment logic
│
├── tasks.py                # Predefined review tasks
├── models.py               # Data models (state, action, observation)
├── inference.py            # Example inference script
├── client.py               # Sample client interaction
│
├── requirements.txt
├── Dockerfile
├── openenv.yaml            # OpenEnv config
└── README.md
```
---
⚙️ Setup Instructions
1️⃣ Clone the repository
```bash
git clone <your-repo-url>
cd code_review_env
```
---
2️⃣ Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows
```
---
3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```
---
4️⃣ Run the server
```bash
python server/app.py
```
OR (recommended):
```bash
uvicorn server.app:app --reload
```
---
🌐 API Usage
🔹 Health Check
GET /health
---
🔹 Reset Environment
POST /reset
Example:
```json
{
  "task_id": "syntax_error"
}
```
---
🔹 Take a Step
POST /step
Example:
```json
{
  "issues": ["Missing semicolon", "Missing bracket"],
  "fixed_code": "corrected code here",
  "submit": false
}
```
---
🔹 Submit Final Review
```json
{
  "issues": ["..."],
  "fixed_code": "...",
  "submit": true
}
```
---
🔹 Get Current State
GET /state
---
🔄 Workflow
Call `/reset` → get a code snippet
Analyze code
Send `/step` with:
issues found
partial or full fix
Repeat until ready
Submit with `"submit": true`
Receive final score 🎯
---
🧪 Example Task
Input Code
```javascript
function calculateTotal(items) {
    let total = 0
    for (let i = 0; i < items.length; i++ {
        total += items[i].price
    }
    return total
}
```
---
🧠 Scoring Logic
Score is calculated based on:
Issue detection accuracy
Code fix similarity
Formula:
Final Score = 0.5 * Issue Score + 0.5 * Fix Similarity
---
📡 WebSocket Support
Endpoint:
/ws
Commands:
```json
{ "command": "reset" }
{ "command": "step", "issues": [], "fixed_code": "", "submit": false }
```
---
🐳 Docker Support
Build:
```bash
docker build -t code-review-env .
```
Run:
```bash
docker run -p 8000:8000 code-review-env
```
---
📌 OpenEnv Compatibility
Step-based interaction
Structured observation/action format
Reward-based evaluation
---
⚠️ Notes for Reviewers
No external API dependency required
Fully self-contained environment
Tasks are predefined in `tasks.py`
Evaluation is deterministic and reproducible
---
👨‍💻 Author
Kavin Kaarthik
---
🏁 Summary
This project demonstrates:
Environment design for AI agents
Code analysis and evaluation logic
API-based interaction system
