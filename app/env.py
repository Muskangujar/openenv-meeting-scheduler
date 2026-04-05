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
            "meeting_duration": self.current_task["duration"],
            "participants": self.current_task["participants"],
            "calendars": self.current_task["calendars"],
            "preferences": self.current_task.get("preferences"),
            "current_proposal": None,
            "history": []
        }

        return Observation(**self.state_data)

    def step(self, action: Action):
        self.steps += 1
        reward = 0.0
        done = False

        if action.action_type == "propose_time":
            if is_valid_slot(action.proposed_time, self.state_data):
                reward += 0.3
                self.state_data["current_proposal"] = action.proposed_time
            else:
                reward -= 0.3

        elif action.action_type == "confirm_meeting":
            if is_perfect_slot(action.proposed_time, self.current_task):
                reward += 0.5
                done = True
            else:
                reward -= 0.4

        elif action.action_type == "cancel":
            reward -= 0.2
            done = True

        if self.steps > 10:
            reward -= 1.0
            done = True

        return Observation(**self.state_data), reward, done, {}

    def state(self):
        return self.state_data