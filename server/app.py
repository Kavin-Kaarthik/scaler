import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional

from server.environment import CodeReviewEnvironment
from models import ReviewAction

app = FastAPI(title="CodeReviewEnv", version="1.0.0")

static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

env = CodeReviewEnvironment()


class ResetRequest(BaseModel):
    task_id: Optional[str] = None


class StepRequest(BaseModel):
    issues: List[str] = []
    fixed_code: str = ""
    submit: bool = False


def obs_to_dict(obs) -> dict:
    return {
        "task_id":           obs.task_id,
        "task_description":  obs.task_description,
        "code_snippet":      obs.code_snippet,
        "language":          obs.language,
        "feedback":          obs.feedback,
        "current_issues":    obs.current_issues,
        "current_fixed_code": obs.current_fixed_code,
        "done":              obs.done,
        "reward":            obs.reward,
        "score":             obs.score,
        "metadata":          obs.metadata,
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/web")
def web_ui():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Web UI not available"}


@app.post("/reset")
def reset(req: ResetRequest = ResetRequest()):
    obs = env.reset(task_id=req.task_id)
    return obs_to_dict(obs)


@app.post("/step")
def step(req: StepRequest):
    action = ReviewAction(
        issues=req.issues,
        fixed_code=req.fixed_code,
        submit=req.submit,
    )
    obs = env.step(action)
    return obs_to_dict(obs)


@app.get("/state")
def state():
    s = env.state
    if s is None:
        return {"error": "No active episode. Call /reset first."}
    return {
        "episode_id":  s.episode_id,
        "step_count":  s.step_count,
        "task_id":     s.task_id,
        "max_steps":   s.max_steps,
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    ws_env = CodeReviewEnvironment()
    try:
        while True:
            raw = await websocket.receive_text()
            msg = json.loads(raw)
            command = msg.get("command", "")

            if command == "reset":
                obs = ws_env.reset(task_id=msg.get("task_id"))
                await websocket.send_text(json.dumps(obs_to_dict(obs)))

            elif command == "step":
                action = ReviewAction(
                    issues=msg.get("issues", []),
                    fixed_code=msg.get("fixed_code", ""),
                    submit=msg.get("submit", False),
                )
                obs = ws_env.step(action)
                await websocket.send_text(json.dumps(obs_to_dict(obs)))

            elif command == "state":
                s = ws_env.state
                if s is None:
                    await websocket.send_text(json.dumps({"error": "Call reset first"}))
                else:
                    await websocket.send_text(json.dumps({
                        "episode_id": s.episode_id,
                        "step_count": s.step_count,
                        "task_id":    s.task_id,
                    }))
            else:
                await websocket.send_text(json.dumps({"error": f"Unknown command: {command}"}))

    except WebSocketDisconnect:
        pass
