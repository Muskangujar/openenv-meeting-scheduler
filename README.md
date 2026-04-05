---
title: Meeting Scheduler Env
emoji: 📅
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860

---

## Description
Simulates real-world meeting scheduling with multiple participants, conflicts, and preferences.

## Tasks
- easy_single_slot: simple scheduling
- medium_conflicts: overlapping conflicts
- hard_preferences: constraints + preferences

## Action Space
- propose_time
- confirm_meeting
- cancel

## Observation Space
- participants
- calendars
- preferences
- current_proposal

## Run Locally
```bash
pip install -r requirements.txt
uvicorn server:app --reload