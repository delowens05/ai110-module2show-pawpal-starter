# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

---

## Smarter Scheduling

New PawPal+ Features!:

- When you mark a daily task (like "morning walk") as done, PawPal+ automatically creates tomorrow's version! No need to manually create it again
- The scheduler spots if you've accidentally scheduled two tasks at the same time and lets you know. You stay in control—the schedule still works, you just get a heads-up to adjust if needed.
-  Quickly see which tasks are pending for a specific pet, or check what's already completed. 
- The scheduler knows your preferences (e.g., "I prefer walks in the morning"). It ranks tasks by urgency first, then fits them into the times you prefer.
- The plan explains its choices when it comes to fitting and scheduling task.

## Testing PawPal+

Run the test suite with:

python -m pytest

Testing covers:

- Ensures tasks are ranked by priority and owner preferences. Tests verify correct ordering when priorities are tied, missing preferences default to medium weight, and empty task lists don't crash.

- Confirms that marking a daily or weekly task as complete automatically creates the next occurrence with the correct due date. Tests verify non-recurring tasks return None, recurring tasks without an initial due date calculate correctly, and all task properties are preserved across occurrences.

- Verifies the scheduler detects overlapping task times and properly flags scheduling conflicts. Tests ensure overlapping tasks are flagged, adjacent non-overlapping tasks are not flagged, partial overlaps are caught, and single-task schedules have no conflicts.


