---

title: Meeting Scheduler Env
emoji: 📅
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
--------------

# Meeting Scheduler OpenEnv

## Overview

This project implements a real-world **meeting scheduling environment** following the OpenEnv specification.
It simulates how assistants, recruiters, and project managers coordinate meetings across multiple participants with conflicting calendars and preferences.

The environment exposes a standard API:

* `reset()`
* `step(action)`
* `state()`

and supports multi-step decision-making with reward feedback.

---

## Objective

The agent must:

* Analyze participant availability
* Propose valid meeting times
* Resolve scheduling conflicts
* Respect user preferences
* Confirm a meeting successfully

---

## Environment API

### `/reset`

Initializes a new scheduling task.

### `/step`

Takes an action and returns:

* observation
* reward
* done flag
* info

### `/state`

Returns the current environment state.

---

## Observation Space

Each observation includes:

* `participants`: list of users
* `calendars`: busy time slots per user
* `preferences`: optional constraints
* `current_proposal`: proposed meeting time
* `history`: action history

---

## Action Space

Supported actions:

* `propose_time` → suggest a meeting time
* `confirm_meeting` → finalize meeting
* `cancel` → cancel scheduling

---

## Tasks

### Easy — Single Slot

* 2 participants
* One valid meeting slot

### Medium — Conflict Resolution

* Multiple participants
* Overlapping conflicts

### Hard — Preferences + Constraints

* Includes user preferences
* Requires optimal scheduling

---

## Reward Design

| Action               | Reward |
| -------------------- | ------ |
| Valid proposal       | +0.3   |
| Invalid proposal     | -0.3   |
| Correct confirmation | +0.5   |
| Wrong confirmation   | -0.4   |
| Step penalty         | -0.01  |
| Too many steps       | -1.0   |

---

## Example Workflow

1. Call `/reset`
2. Propose a valid time
3. Confirm meeting
4. Receive final reward

---

## Baseline Results

```text
Easy Task:    1.00
Medium Task:  1.00
Hard Task:    0.60
```

---

## Project Structure

```
app/
  env.py
  models.py
  tasks.py
  utils.py
  graders.py

server.py
inference.py
requirements.txt
Dockerfile
openenv.yaml
README.md
```

---

## Run Locally

```bash
pip install -r requirements.txt
uvicorn server:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

## Run Inference

```bash
python inference.py
```

---

## Docker

```bash
docker build -t meeting-env .
docker run -p 7860:7860 meeting-env
```

Open:

```
http://localhost:7860/docs
```

---

## Deployment

The environment is deployed on Hugging Face Spaces using Docker.

---

## Why This Matters

Meeting scheduling is a real-world problem involving:

* constraint satisfaction
* multi-agent coordination
* decision-making under uncertainty

This environment provides a benchmark for evaluating such capabilities.

---

## License

Apache 2.0 License
