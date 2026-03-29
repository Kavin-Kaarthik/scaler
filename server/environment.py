import uuid
from typing import List, Optional

from models import ReviewAction, ReviewObservation, ReviewState
from tasks import TASKS, TASK_MAP, grade


class CodeReviewEnvironment:
    MAX_STEPS = 10

    def __init__(self):
        self._state: Optional[ReviewState] = None
        self._task = None
        self._issues: List[str] = []
        self._fixed_code: str = ""
        self._feedback: List[str] = []
        self._task_index: int = 0

    def reset(self, task_id: Optional[str] = None) -> ReviewObservation:
        if task_id and task_id in TASK_MAP:
            self._task = TASK_MAP[task_id]
        else:
            self._task = TASKS[self._task_index % len(TASKS)]
            self._task_index += 1

        self._issues = []
        self._fixed_code = ""
        self._feedback = ["New code review task loaded. Analyze the code and submit your review."]

        self._state = ReviewState(
            episode_id=str(uuid.uuid4()),
            step_count=0,
            task_id=self._task["id"],
            max_steps=self.MAX_STEPS,
        )

        return self._make_obs(done=False, reward=0.0)

    def step(self, action: ReviewAction) -> ReviewObservation:
        if self._state is None:
            raise RuntimeError("Call reset() before step()")

        self._state.step_count += 1
        self._feedback = []

        if action.issues:
            self._issues = action.issues
            self._feedback.append(f"Recorded {len(action.issues)} issue(s).")

        if action.fixed_code.strip():
            self._fixed_code = action.fixed_code
            self._feedback.append("Fixed code recorded.")

        if action.submit:
            score = grade(self._state.task_id, self._issues, self._fixed_code)
            self._feedback.append(f"Review submitted. Score: {score:.4f}")
            return self._make_obs(done=True, reward=score, score=score)

        if self._state.step_count >= self.MAX_STEPS:
            score = grade(self._state.task_id, self._issues, self._fixed_code)
            self._feedback.append(f"Max steps reached. Score: {score:.4f}")
            return self._make_obs(done=True, reward=score, score=score)

        current_score = grade(self._state.task_id, self._issues, self._fixed_code)
        partial_reward = current_score * 0.1
        return self._make_obs(done=False, reward=partial_reward, score=current_score)

    @property
    def state(self) -> ReviewState:
        return self._state

    def _make_obs(self, done: bool, reward: float, score: float = None) -> ReviewObservation:
        if score is None:
            score = grade(self._state.task_id, self._issues, self._fixed_code)
        return ReviewObservation(
            task_id=self._task["id"],
            task_description=self._task["description"],
            code_snippet=self._task["code"],
            language=self._task["language"],
            feedback=list(self._feedback),
            current_issues=list(self._issues),
            current_fixed_code=self._fixed_code,
            done=done,
            reward=reward,
            score=score,
            metadata={
                "step_count": self._state.step_count,
                "max_steps": self.MAX_STEPS,
                "task_id": self._state.task_id,
            },
        )
