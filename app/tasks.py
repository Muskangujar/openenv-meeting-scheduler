def load_task(task_name: str):

    if task_name == "easy_single_slot":
        return {
            "participants": ["alice", "bob"],
            "calendars": {
                "alice": ["10:00-11:00"],
                "bob": ["11:00-12:00"]
            },
            "duration": 60,
            "correct_slot": "12:00-13:00"
        }

    elif task_name == "medium_conflicts":
        return {
            "participants": ["alice", "bob", "charlie"],
            "calendars": {
                "alice": ["10:00-11:00"],
                "bob": ["10:30-11:30"],
                "charlie": ["11:00-12:00"]
            },
            "duration": 60,
            "correct_slot": "12:00-13:00"
        }

    elif task_name == "hard_preferences":
        return {
            "participants": ["alice", "bob", "charlie"],
            "calendars": {
                "alice": ["9:00-10:00"],
                "bob": ["10:00-11:00"],
                "charlie": ["11:00-12:00"]
            },
            "preferences": {
                "alice": "no_morning"
            },
            "duration": 60,
            "correct_slot": "13:00-14:00"
        }