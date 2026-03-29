def is_valid_slot(slot, state):
    # basic check: not in any busy slots
    for user, busy_slots in state["calendars"].items():
        if slot in busy_slots:
            return False
    return True


def is_perfect_slot(slot, task):
    # simple rule: valid + not violating preferences
    if not is_valid_slot(slot, task):
        return False

    prefs = task.get("preferences", {})
    if prefs.get("alice") == "no_morning" and slot.startswith("09"):
        return False

    return True