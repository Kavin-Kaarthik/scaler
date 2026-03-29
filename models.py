from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ReviewAction:
    issues: List[str] = field(default_factory=list)
    fixed_code: str = ""
    submit: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReviewObservation:
    task_id: str
    task_description: str
    code_snippet: str
    language: str
    feedback: List[str]
    current_issues: List[str]
    current_fixed_code: str
    done: bool = False
    reward: float = 0.0
    score: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReviewState:
    episode_id: str = ""
    step_count: int = 0
    task_id: str = ""
    max_steps: int = 10
