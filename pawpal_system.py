from dataclasses import dataclass
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


@dataclass
class Task:
    name: str
    category: str
    duration: int
    priority: int
    frequency: str = "daily"
    preferred_time: str = "anytime"
    pet_specific: bool = False
    completed: bool = False

    def is_due_today(self) -> bool:
        """Return True when this task should be done today."""
        # For simplicity, assume daily tasks are always due
        return self.frequency == "daily"

    def get_description(self) -> str:
        """Return a brief string describing this task."""
        return f"{self.name} ({self.category}, {self.duration} min, priority {self.priority})"

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True


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
