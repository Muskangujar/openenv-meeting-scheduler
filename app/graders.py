from app.utils import is_valid_slot, is_perfect_slot

def _is_functionally_correct(slot, task):
    """Checks if the slot perfectly satisfies calendars and preferences."""
    return is_perfect_slot(slot, task)

def grade_easy(trajectory, task):
    """Expect agent to pick any valid, preference-respecting slot and confirm it."""
    for step in trajectory:
        if step["action"] == "confirm_meeting":
            if step.get("proposed_time") and _is_functionally_correct(step.get("proposed_time"), task):
                return 0.99
    return 0.01

def grade_medium(trajectory, task):
    """
    Score components:
    - Finds valid slot and confirms (0.6)
    - Low step count / efficiency (0.2)
    - Avoids unnecessary cancellations (0.2)
    """
    score = 0.0
    confirmed = False
    
    for step in trajectory:
        if step["action"] == "confirm_meeting":
            if step.get("proposed_time") and _is_functionally_correct(step.get("proposed_time"), task):
                confirmed = True

    if confirmed:
        score += 0.6

    if len(trajectory) <= 6:
        score += 0.2

    bad_actions = any(s["action"] in ["cancel", "reschedule"] for s in trajectory)
    if not bad_actions:
        score += 0.2

    return max(0.01, min(score, 0.99))

def grade_hard(trajectory, task):
    """
    Evaluates complex preference satisfaction.
    Score components:
    - Confirms a valid slot (0.4)
    - Fully respects soft preferences (0.4)
    - Efficiency (0.2)
    """
    score = 0.0
    confirmed_slot = None
    
    for step in trajectory:
        if step["action"] == "confirm_meeting":
            confirmed_slot = step.get("proposed_time")

    if confirmed_slot and is_valid_slot(confirmed_slot, task.get("calendars", {})):
        # Valid slot (hard constraints met)
        score += 0.4
        
        # Soft constraints met
        if is_perfect_slot(confirmed_slot, task):
            score += 0.4

    if len(trajectory) <= 10:
        score += 0.2

    return max(0.01, min(score, 0.99))

