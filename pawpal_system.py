from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class Pet:
    name: str
    species: str
    age: int
    breed: Optional[str] = None
    special_needs: List[str] = None

    def __post_init__(self):
        if self.special_needs is None:
            self.special_needs = []

    def get_info(self) -> str:
        pass

    def has_need(self, need: str) -> bool:
        pass


@dataclass
class Owner:
    name: str
    available_time: Dict[str, tuple]
    preferences: Dict[str, str]
    pets: List[Pet] = None

    def __post_init__(self):
        if self.pets is None:
            self.pets = []

    def get_available_slots(self, day: str) -> list:
        pass

    def get_preference_weight(self, task_category: str) -> int:
        pass


@dataclass
class Task:
    name: str
    category: str
    duration: int
    priority: int
    frequency: str = "daily"
    preferred_time: str = "anytime"
    pet_specific: bool = False

    def is_due_today(self) -> bool:
        pass

    def get_description(self) -> str:
        pass


class Schedule:
    def __init__(self, date: str, owner: Owner, pet: Pet):
        self.date = date
        self.scheduled_tasks: List[Dict] = []
        self.total_time: int = 0
        self.owner = owner
        self.pet = pet

    def add_task(self, task: Task, start_time: str, reason: str):
        pass

    def get_plan_summary(self) -> list:
        pass

    def explain_plan(self) -> str:
        pass

    def generate_plan(self, owner: Owner, pet: Pet, tasks: List[Task], available_time: Dict[str, tuple]) -> 'Schedule':
        pass

    def sort_tasks(self, tasks: List[Task], owner_preferences: Dict[str, str]) -> List[Task]:
        pass

    def fit_into_schedule(self, sorted_tasks: List[Task], available_slots: list) -> list:
        pass
