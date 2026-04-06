def grade_easy(trajectory, task):
    """
    Expect: agent picks correct free slot and confirms
    """
    correct_slot = task.get("correct_slot")
    confirmed = False

    for step in trajectory:
        if step["action"] == "confirm_meeting":
            if step.get("proposed_time") == correct_slot:
                confirmed = True

    return 1.0 if confirmed else 0.0


def grade_medium(trajectory, task):
    """
    Score:
    - valid slot (0.6)
    - reasonable steps (0.2)
    - no bad actions (0.2)
    """
    score = 0.0
    correct_slot = task.get("correct_slot")

    confirmed = False
    steps = len(trajectory)

    for step in trajectory:
        if step["action"] == "confirm_meeting":
            if step.get("proposed_time") == correct_slot:
                confirmed = True

    if confirmed:
        score += 0.6

    if steps <= 6:
        score += 0.2

    bad_actions = any(s["action"] == "cancel" for s in trajectory)
    if not bad_actions:
        score += 0.2

    return min(score, 1.0)


def grade_hard(trajectory, task):
    """
    Score:
    - valid slot (0.4)
    - respects preferences (0.3)
    - efficient (0.3)
    """
    score = 0.0
    correct_slot = task.get("correct_slot")

    confirmed = False
    respected_preferences = True

    for step in trajectory:
        if step["action"] == "confirm_meeting":
            if step.get("proposed_time") == correct_slot:
                confirmed = True

            # Example preference check
            if step.get("proposed_time", "").startswith("09"):
                respected_preferences = False

    if confirmed:
        score += 0.4

    if respected_preferences:
        score += 0.3

    if len(trajectory) <= 7:
        score += 0.3

    return min(score, 1.0)