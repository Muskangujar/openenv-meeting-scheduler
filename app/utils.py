from datetime import datetime
from typing import Dict, Any, List

def parse_time(t_str: str) -> datetime:
    return datetime.strptime(t_str.strip(), "%H:%M")

def is_overlap(slot1: str, slot2: str) -> bool:
    try:
        s1_start, s1_end = [parse_time(t) for t in slot1.split("-")]
        s2_start, s2_end = [parse_time(t) for t in slot2.split("-")]
        return max(s1_start, s2_start) < min(s1_end, s2_end)
    except ValueError:
        return False

def is_valid_slot(slot: str, calendars: Dict[str, List[str]]) -> bool:
    """Check if the slot overlaps with any busy slot across all calendars."""
    for user, busy_slots in calendars.items():
        for busy in busy_slots:
            if is_overlap(slot, busy):
                return False
    return True

def satisfies_preferences(slot: str, user: str, preference: str) -> bool:
    try:
        start_t = parse_time(slot.split("-")[0])
        end_t = parse_time(slot.split("-")[1])
        
        # Soft constraints map
        if preference == "no_morning" and start_t.hour < 12:
            return False
        if preference == "afternoon_only" and (start_t.hour < 12 or end_t.hour > 18):
            return False
        if preference == "no_late_meetings" and end_t.hour > 17:
            return False
    except ValueError:
        pass
    return True

def is_perfect_slot(slot: str, task: Dict[str, Any]) -> bool:
    """Validates hard constraints (calendars) and soft constraints (preferences)."""
    if not is_valid_slot(slot, task.get("calendars", {})):
        return False
        
    prefs = task.get("preferences", {})
    for user, pref in prefs.items():
        if not satisfies_preferences(slot, user, pref):
            return False
            
    return True