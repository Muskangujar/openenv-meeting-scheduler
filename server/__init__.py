# server/__init__.py
from fastapi import FastAPI
from app.env import MeetingSchedulerEnv
from app.models import Action

app = FastAPI()
env = MeetingSchedulerEnv()

@app.post("/reset")
def reset(task: str = "easy_single_slot"):
    obs = env.reset(task)
    return obs.dict()

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.dict(),
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

# For OpenEnv validation
main = app

# For ASGI - make the module act as the app
__all__ = ['app', 'main']