import os
from openai import OpenAI

client = OpenAI(
    base_url=os.getenv("API_BASE_URL", "https://api.openai.com/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "dummy-key"),
)

MODEL = os.getenv("MODEL_NAME", "gpt-4o-mini")

from app.env import MeetingSchedulerEnv

def simple_policy(obs):
    """
    VERY basic baseline:
    always propose 12:00-13:00 then confirm
    """

    if obs.current_proposal is None:
        return {
            "action_type": "propose_time",
            "proposed_time": "12:00-13:00"
        }
    else:
        return {
            "action_type": "confirm_meeting",
            "proposed_time": obs.current_proposal
        }


def run_task(env, task_name):
    obs = env.reset(task_name)
    trajectory = []

    for _ in range(10):
        action = simple_policy(obs)

        trajectory.append({
            "action": action["action_type"],
            "proposed_time": action.get("proposed_time")
        })

        obs, reward, done, _ = env.step(type("A", (), action))

        if done:
            break

    return trajectory


def main():
    env = MeetingSchedulerEnv()

    from app.graders import grade_easy, grade_medium, grade_hard

    tasks = [
        ("easy_single_slot", grade_easy),
        ("medium_conflicts", grade_medium),
        ("hard_preferences", grade_hard)
    ]

    results = {}

    for task_name, grader in tasks:
        traj = run_task(env, task_name)
        score = grader(traj, env.current_task)
        results[task_name] = score

    print("\nBaseline Results:")
    for k, v in results.items():
        print(f"{k}: {v:.2f}")


if __name__ == "__main__":
    main()