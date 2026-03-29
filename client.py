import requests
from typing import List, Optional
from models import ReviewAction, ReviewObservation


class CodeReviewEnvClient:
    def __init__(self, base_url: str = "http://localhost:7860"):
        self.base_url = base_url.rstrip("/")

    def reset(self, task_id: Optional[str] = None) -> ReviewObservation:
        payload = {}
        if task_id:
            payload["task_id"] = task_id
        r = requests.post(f"{self.base_url}/reset", json=payload)
        r.raise_for_status()
        return self._parse(r.json())

    def step(self, action: ReviewAction) -> ReviewObservation:
        payload = {
            "issues":     action.issues,
            "fixed_code": action.fixed_code,
            "submit":     action.submit,
        }
        r = requests.post(f"{self.base_url}/step", json=payload)
        r.raise_for_status()
        return self._parse(r.json())

    def state(self) -> dict:
        r = requests.get(f"{self.base_url}/state")
        r.raise_for_status()
        return r.json()

    def health(self) -> bool:
        try:
            r = requests.get(f"{self.base_url}/health", timeout=5)
            return r.json().get("status") == "healthy"
        except Exception:
            return False

    @staticmethod
    def _parse(data: dict) -> ReviewObservation:
        return ReviewObservation(
            task_id=data["task_id"],
            task_description=data["task_description"],
            code_snippet=data["code_snippet"],
            language=data["language"],
            feedback=data["feedback"],
            current_issues=data["current_issues"],
            current_fixed_code=data["current_fixed_code"],
            done=data["done"],
            reward=data["reward"],
            score=data["score"],
            metadata=data.get("metadata", {}),
        )
