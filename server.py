from fastapi import FastAPI
from app.env import MeetingSchedulerEnv
from app.models import Action

app = FastAPI()
env = MeetingSchedulerEnv()


@app.post("/reset")
def reset(task: str = "easy_single_slot"):
    return env.reset(task)   # ✅ return object directly


@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs,   # ✅ no .dict()
        "reward": reward,
        "done": done,
        "info": info
    }


@app.get("/state")
def state():
    return env.state()


@app.get("/")
def home():
    return {"message": "Meeting Scheduler API is running"}