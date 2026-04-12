import uuid
from app.models import Observation, Action
from app.tasks import load_task
from app.utils import is_valid_slot, is_perfect_slot

class MeetingSchedulerEnv:
    def __init__(self):
        self.state_data = None
        self.current_task = None
        self.steps = 0

    def reset(self, task_name: str = "easy_single_slot"):
        self.current_task = load_task(task_name)
        self.steps = 0

        self.state_data = {
            "request_id": str(uuid.uuid4()),
            "meeting_duration": self.current_task.get("duration", 60),
            "participants": self.current_task.get("participants", []),
            "calendars": self.current_task.get("calendars", {}),
            "preferences": self.current_task.get("preferences", {}),
            "current_proposal": None,
            "history": []
        }

        return Observation(**self.state_data)

    def step(self, action: Action):
        self.steps += 1
        reward = 0.0
        done = False
        info = {"msg": ""}

        # Action history logging
        action_desc = f"{action.action_type}"
        if action.proposed_time:
            action_desc += f" time={action.proposed_time}"
        self.state_data["history"].append(action_desc)

        if action.action_type == "propose_time":
            if not action.proposed_time:
                reward -= 0.5
                info["msg"] = "Missing proposed_time."
            elif is_valid_slot(action.proposed_time, self.state_data["calendars"]):
                reward += 0.3
                self.state_data["current_proposal"] = action.proposed_time
                info["msg"] = "Proposal valid and recorded."
            else:
                reward -= 0.3
                info["msg"] = "Proposal overlaps with busy slots."

        elif action.action_type == "confirm_meeting":
            if not action.proposed_time:
                reward -= 0.5
                info["msg"] = "Missing proposed_time to confirm."
            elif is_perfect_slot(action.proposed_time, self.current_task):
                reward += 1.0
                done = True
                info["msg"] = "Meeting scheduled successfully!"
            else:
                reward -= 0.4
                info["msg"] = "Slot confirmed but it violates constraints or preferences."

        elif action.action_type == "cancel":
            reward -= 0.5
            done = True
            info["msg"] = "Meeting cancelled."
            
        elif action.action_type == "check_conflict":
             reward += 0.05
             info["msg"] = "Checked calendar constraints."

        elif action.action_type == "reschedule":
             reward -= 0.1
             info["msg"] = "Rescheduling penalty applied."

        if self.steps >= 15:  # Maximum 15 negotiation steps allowed
            reward -= 1.0
            done = True
            info["msg"] = "Max iterative steps reached for scheduling."

        return Observation(**self.state_data), reward, done, info

    def state(self):
        return self.state_data