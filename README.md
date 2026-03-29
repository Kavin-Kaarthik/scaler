# CodeReviewEnv

An OpenEnv RL environment where an AI agent reviews code in any programming language — identifying bugs, style issues, and logic errors, then providing corrected code.

## Tasks

| ID | Language | Difficulty | Description |
|---|---|---|---|
| `syntax_error` | JavaScript | Easy | Missing semicolons, unclosed parenthesis |
| `logic_bug` | Python | Medium | Wrong array index returning incorrect value |
| `full_review` | Java | Hard | Naming violations, O(n²) complexity, poor practices |

## Action Space

| Field | Type | Description |
|---|---|---|
| `issues` | `List[str]` | List of identified problems |
| `fixed_code` | `str` | Corrected code |
| `submit` | `bool` | Submit the review for grading |

## Observation Space

| Field | Type | Description |
|---|---|---|
| `task_id` | `str` | Current task |
| `task_description` | `str` | What the agent must do |
| `code_snippet` | `str` | The code to review |
| `language` | `str` | Programming language |
| `feedback` | `List[str]` | Environment messages |
| `done` | `bool` | Episode complete |
| `reward` | `float` | Step reward |
| `score` | `float` | Score 0.0–1.0 |

## Grading

- **50%** keyword match — did the agent identify the right type of issue?
- **50%** diff similarity — how close is the fix to the expected solution?

## Setup

```bash
pip install -r requirements.txt
uvicorn server.app:app --host 0.0.0.0 --port 7860 --reload
```

## Docker

```bash
docker build -t code_review_env .
docker run -p 7860:7860 code_review_env
```

## Inference

```bash
set API_BASE_URL=https://router.huggingface.co/v1
set HF_TOKEN=hf_your_token_here
set MODEL_NAME=meta-llama/Llama-3.1-8B-Instruct
set ENV_BASE_URL=http://localhost:7860
python inference.py
```

## Baseline Scores

| Task | Score |
|---|---|
| syntax_error | ~0.65 |
| logic_bug | ~0.70 |
| full_review | ~0.45 |
| **Average** | **~0.60** |
