# server/app.py
from fastapi import FastAPI
from app.env import MeetingSchedulerEnv
from app.models import Action

app = FastAPI()
env = MeetingSchedulerEnv()

@app.post("/reset")
def reset(task: str = "easy_single_slot"):
    obs = env.reset(task)
    return obs.model_dump()

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.model_dump(),
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

def main():
    """Required by OpenEnv validation"""
    return app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)