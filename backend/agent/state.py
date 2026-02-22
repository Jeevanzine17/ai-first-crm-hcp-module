from typing import TypedDict, Optional, Dict

class AgentState(TypedDict):
    user_input: str
    intent: Optional[str]
    response: Optional[str]