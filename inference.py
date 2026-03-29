import os
import json
import re
import sys
from dotenv import load_dotenv
from openai import OpenAI
from client import CodeReviewEnvClient
from models import ReviewAction
from tasks import TASKS

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
API_KEY      = os.getenv("HF_TOKEN") or os.getenv("API_KEY", "")
MODEL_NAME   = os.getenv("MODEL_NAME", "meta-llama/Llama-3.1-8B-Instruct")
ENV_BASE_URL = os.getenv("ENV_BASE_URL", "http://localhost:7860")

MAX_STEPS   = 3
TEMPERATURE = 0.2
MAX_TOKENS  = 1024

llm = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
env = CodeReviewEnvClient(base_url=ENV_BASE_URL)

SYSTEM_PROMPT = """You are an expert code reviewer who reviews code in any programming language.

You will be given a code snippet to review.

Respond ONLY with a valid JSON object in this exact format:
{
  "issues": ["issue 1 description", "issue 2 description"],
  "fixed_code": "the fully corrected code here"
}

No explanation. No markdown. No code blocks. Just the raw JSON object."""


def call_llm(code: str, language: str, task_description: str) -> dict:
    user_prompt = (
        f"Language: {language}\n\n"
        f"Task: {task_description}\n\n"
        f"Code to review:\n{code}\n\n"
        "Respond with JSON only."
    )
    response = llm.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_prompt},
        ],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )
    text = response.choices[0].message.content.strip()
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON in model output: {text!r}")
    return json.loads(match.group())


def run_episode(task_id: str) -> float:
    obs = env.reset(task_id=task_id)
    print(f"\n{'='*60}\nTask : {task_id} ({obs.language})")
    print(f"Goal : {obs.task_description[:100]}...")

    try:
        result     = call_llm(obs.code_snippet, obs.language, obs.task_description)
        issues     = result.get("issues", [])
        fixed_code = result.get("fixed_code", "")
        print(f"Issues found : {len(issues)}")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
    except Exception as e:
        print(f"LLM error: {e}")
        issues, fixed_code = [], ""

    obs = env.step(ReviewAction(issues=issues, fixed_code=fixed_code))
    obs = env.step(ReviewAction(submit=True))

    print(f"Score: {obs.score:.4f}")
    return obs.score


def main():
    print("CodeReviewEnv — Inference Script")
    print(f"Model : {MODEL_NAME}")
    print(f"Server: {ENV_BASE_URL}")

    if not env.health():
        print(f"ERROR: Server at {ENV_BASE_URL} is not responding.")
        print("Make sure the server is running: uvicorn server.app:app --host 0.0.0.0 --port 7860")
        sys.exit(1)

    scores = {}
    for task in TASKS:
        try:
            scores[task["id"]] = run_episode(task["id"])
        except Exception as e:
            print(f"Episode failed for {task['id']}: {e}")
            scores[task["id"]] = 0.0

    print(f"\n{'='*60}\nFINAL RESULTS")
    print(f"{'='*60}")
    total = 0.0
    for task_id, score in scores.items():
        print(f"  {task_id:<20} {score:.4f}")
        total += score
    avg = total / len(scores)
    print(f"  {'AVERAGE':<20} {avg:.4f}")
    print(f"{'='*60}")

    with open("results.json", "w") as f:
        json.dump({"scores": scores, "average": avg, "model": MODEL_NAME}, f, indent=2)
    print("Results saved to results.json")


if __name__ == "__main__":
    main()