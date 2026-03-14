from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AgentMemory:
    episodic: list[dict] = field(default_factory=list)
    semantic: dict[str, float] = field(default_factory=dict)
    strategic: list[str] = field(default_factory=list)

    def append_event(self, event: dict) -> None:
        self.episodic.append(event)

    def update_beliefs(self, observation: dict) -> None:
        for key, value in observation.items():
            self.semantic[key] = float(value)

    def record_plan(self, plan: str) -> None:
        self.strategic.append(plan)

    def summarize_recent(self, n: int) -> list[dict]:
        return self.episodic[-n:]

    def retrieve_salient_context(self, context_key: str):
        return self.semantic.get(context_key)
