from pydantic import BaseModel
from typing import List, Dict, Optional, Literal

# ------------------------
# Observation
# ------------------------
class Observation(BaseModel):
    request_id: str
    meeting_duration: int
    participants: List[str]
    calendars: Dict[str, List[str]]
    preferences: Optional[Dict[str, str]] = None
    current_proposal: Optional[str] = None
    history: List[str]


# ------------------------
# Action
# ------------------------
class Action(BaseModel):
    action_type: Literal[
        "propose_time",
        "check_conflict",
        "reschedule",
        "confirm_meeting",
        "cancel"
    ]
    proposed_time: Optional[str] = None
    participant: Optional[str] = None


# ------------------------
# Reward
# ------------------------
class Reward(BaseModel):
    score: float
    reason: str