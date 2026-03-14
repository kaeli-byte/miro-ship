from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AgentMemory:
    episodic: list[dict] = field(default_factory=list)
    semantic: dict[str, float] = field(default_factory=dict)
    strategic: list[str] = field(default_factory=list)

    def append_event(self, event: dict) -> None:
        """
        Append an event record to the episodic memory.
        
        Parameters:
            event (dict): Dictionary representing an event or observation to store in episodic memory.
        """
        self.episodic.append(event)

    def update_beliefs(self, observation: dict) -> None:
        """
        Update the semantic belief store with values from an observation mapping.
        
        Each key in `observation` is stored in the instance's `semantic` dictionary with its value converted to a `float`.
        
        Parameters:
            observation (dict): Mapping of belief names to numeric values (or values convertible to `float`).
        """
        for key, value in observation.items():
            self.semantic[key] = float(value)

    def record_plan(self, plan: str) -> None:
        """
        Record a strategy or plan string in the agent's strategic memory.
        
        Parameters:
            plan (str): A textual representation of a plan or strategy to append to the strategic history.
        """
        self.strategic.append(plan)

    def summarize_recent(self, n: int) -> list[dict]:
        """
        Retrieve the most recent episodic events.
        
        Parameters:
            n (int): Number of most-recent events to return; should be a positive integer.
        
        Returns:
            list[dict]: The last n entries from episodic memory; if n exceeds the number of stored events, returns all events.
        """
        return self.episodic[-n:]

    def retrieve_salient_context(self, context_key: str):
        """
        Retrieve the stored semantic value associated with a context key.
        
        Parameters:
            context_key (str): The key identifying the semantic belief or context.
        
        Returns:
            float | None: The numeric belief value for the given key, or `None` if the key is not present.
        """
        return self.semantic.get(context_key)
