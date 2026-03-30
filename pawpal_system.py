from dataclasses import dataclass
from datetime import date, timedelta
from typing import List, Dict, Optional


@dataclass
class Pet:
    name: str
    species: str
    age: int
    breed: Optional[str] = None
    special_needs: List[str] = None
    tasks: List['Task'] = None

    def __post_init__(self):
        """Initialize default lists after dataclass creation."""
        if self.special_needs is None:
            self.special_needs = []
        if self.tasks is None:
            self.tasks = []

    def get_info(self) -> str:
        """Return a short summary of this pet."""
        breed_info = f" ({self.breed})" if self.breed else ""
        needs_info = f" with special needs: {', '.join(self.special_needs)}" if self.special_needs else ""
        return f"{self.name} is a {self.age}-year-old {self.species}{breed_info}{needs_info}."

    def has_need(self, need: str) -> bool:
        """Check if this pet has a specific special need."""
        return need in self.special_needs


@dataclass
class Owner:
    name: str
    available_time: Dict[str, tuple]
    preferences: Dict[str, str]
    pets: List[Pet] = None

    def __post_init__(self):
        """Initialize default pets list after dataclass creation."""
        if self.pets is None:
            self.pets = []

    def get_available_slots(self, day: str) -> List[tuple[int, int]]:
        """Return available time slots for the owner."""
        # Assuming available_time is daily slots like {"morning": (8,12), ...}
        # For simplicity, ignore 'day' and return all slots
        return list(self.available_time.values())

    def get_preference_weight(self, task_category: str) -> int:
        """Return priority weight for a task category based on preferences."""
        pref = self.preferences.get(task_category, "medium")
        weights = {"high": 3, "medium": 2, "low": 1}
        return weights.get(pref, 2)

    def get_all_tasks(self) -> List['Task']:
        """Collect tasks from all pets owned by this owner."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def filter_tasks(self, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List['Task']:
        """Return tasks filtered by completion status and/or pet name."""
        filtered = []
        for pet in self.pets:
            if pet_name is not None and pet.name != pet_name:
                continue
            for task in pet.tasks:
                if completed is not None and task.completed != completed:
                    continue
                filtered.append(task)
        return filtered


@dataclass
class Task:
    name: str
    category: str
    duration: int
    priority: int
    frequency: str = "daily"  # one of "daily", "weekly", "none"
    preferred_time: str = "anytime"
    pet_specific: bool = False
    completed: bool = False
    due_date: Optional[date] = None

    def is_due_today(self) -> bool:
        """Return True when this task should be done today."""
        if self.due_date:
            return self.due_date == date.today()
        return self.frequency == "daily"

    def get_description(self) -> str:
        """Return a brief string describing this task."""
        due = f", due {self.due_date.isoformat()}" if self.due_date else ""
        return f"{self.name} ({self.category}, {self.duration} min, priority {self.priority}{due})"

    def mark_complete(self) -> Optional['Task']:
        """Mark this task complete and create the next occurrence for daily/weekly recurrence."""
        self.completed = True

        if self.frequency not in ("daily", "weekly"):
            return None

        if self.due_date is None:
            next_date = date.today()
        else:
            next_date = self.due_date

        if self.frequency == "daily":
            next_date = next_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = next_date + timedelta(weeks=1)

        return Task(
            name=self.name,
            category=self.category,
            duration=self.duration,
            priority=self.priority,
            frequency=self.frequency,
            preferred_time=self.preferred_time,
            pet_specific=self.pet_specific,
            completed=False,
            due_date=next_date,
        )


class Schedule:
    def __init__(self, date: str, owner: Owner, pet: Pet):
        self.date = date
        self.scheduled_tasks: List[Dict] = []
        self.total_time: int = 0
        self.owner = owner
        self.pet = pet

    def add_task(self, task: 'Task', start_time: str, reason: str):
        """Add a task to the schedule with a start time and a reason."""
        # Assume start_time is like "08:00", duration in minutes
        # For simplicity, calculate end_time by adding duration (ignoring hours format)
        # In real impl, parse time properly
        end_time = f"{int(start_time.split(':')[0]) + task.duration // 60}:{task.duration % 60:02d}"  # Rough
        self.scheduled_tasks.append({
            "task": task,
            "start_time": start_time,
            "end_time": end_time,
            "reason": reason
        })
        self.total_time += task.duration

    def get_plan_summary(self) -> List[Dict]:
        """Return the raw schedule entries."""
        return self.scheduled_tasks

    def explain_plan(self) -> str:
        """Return a human-readable explanation of why tasks were chosen."""
        if not self.scheduled_tasks:
            return "No tasks were scheduled due to time constraints or lack of due tasks."
        reasons = [f"- {entry['task'].name}: {entry['reason']}" for entry in self.scheduled_tasks]
        return f"Daily plan for {self.date}: Tasks prioritized by priority and owner preferences, fitted into available time slots.\n" + "\n".join(reasons)

    @classmethod
    def generate_plan(cls, date: str, owner: Owner) -> 'Schedule':
        """Create and return a schedule for the owner from all pet tasks."""
        # Assume one pet for simplicity, or handle multiple
        pet = owner.pets[0] if owner.pets else None
        schedule = cls(date, owner, pet)
        tasks = owner.get_all_tasks()
        sorted_tasks = schedule.sort_tasks(tasks, owner.preferences)
        available_slots = list(owner.available_time.values())
        fitted_tasks = schedule.fit_into_schedule(sorted_tasks, available_slots)
        for entry in fitted_tasks:
            schedule.add_task(entry["task"], entry["start_time"], entry["reason"])
        return schedule

    @classmethod
    def generate_plan_with_warnings(cls, date: str, owner: Owner) -> tuple['Schedule', List[str]]:
        """Generate a schedule and return it with a list of warning messages (non-blocking)."""
        schedule = cls.generate_plan(date, owner)
        warnings = []

        conflicts = schedule.detect_scheduling_conflicts()
        for c in conflicts:
            warning_msg = f"⚠️  '{c['task1']}' ({c['pet1']}) overlaps '{c['task2']}' ({c['pet2']}) at {c['overlap']}"
            warnings.append(warning_msg)

        return schedule, warnings


    def sort_tasks(self, tasks: List['Task'], owner_preferences: Dict[str, str]) -> List['Task']:
        """Sort tasks by priority and owner preferences."""
        def sort_key(task):
            pref_weight = self.owner.get_preference_weight(task.category) if self.owner else 2
            return (-task.priority, -pref_weight)  # Higher priority and pref first
        return sorted(tasks, key=sort_key)
    

    def fit_into_schedule(self, sorted_tasks: List['Task'], available_slots: List[tuple[int, int]]) -> List[Dict]:
        """Fit sorted tasks into available time slots."""
        scheduled = []
        for task in sorted_tasks:
            if not task.is_due_today():
                continue
            for slot_start, slot_end in available_slots:
                slot_duration = (slot_end - slot_start) * 60  # in minutes
                if task.duration <= slot_duration:
                    start_time = f"{slot_start}:00"
                    reason = f"Scheduled in {slot_start}-{slot_end} slot due to high priority ({task.priority}) and preference for {task.category}."
                    scheduled.append({"task": task, "start_time": start_time, "reason": reason})
                    break  # Assign to first fitting slot
        return scheduled

    def _time_to_minutes(self, time_str: str) -> int:
        """Convert HH:MM string to total minutes since midnight."""
        parts = time_str.split(":")
        return int(parts[0]) * 60 + int(parts[1])

    def detect_scheduling_conflicts(self) -> List[Dict]:
        """Detect tasks scheduled at overlapping times and return list of conflicts."""
        conflicts = []
        tasks = self.scheduled_tasks
        for i, entry1 in enumerate(tasks):
            for entry2 in tasks[i + 1 :]:
                start1 = self._time_to_minutes(entry1["start_time"])
                start2 = self._time_to_minutes(entry2["start_time"])
                end1 = self._time_to_minutes(entry1["end_time"])
                end2 = self._time_to_minutes(entry2["end_time"])

                # Check for overlap: start of one is before end of other
                if (start1 < end2) and (start2 < end1):
                    pet1_name = next((p.name for p in self.owner.pets if entry1["task"] in p.tasks), "unknown")
                    pet2_name = next((p.name for p in self.owner.pets if entry2["task"] in p.tasks), "unknown")
                    conflicts.append(
                        {
                            "task1": entry1["task"].name,
                            "pet1": pet1_name,
                            "task2": entry2["task"].name,
                            "pet2": pet2_name,
                            "overlap": f"{entry1['start_time']}-{min(end1, end2) // 60}:{min(end1, end2) % 60:02d}",
                        }
                    )
        return conflicts

