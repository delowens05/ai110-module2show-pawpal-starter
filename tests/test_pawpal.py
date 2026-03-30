import unittest
from datetime import date, timedelta
from pawpal_system import Pet, Owner, Task, Schedule


class TestPawPal(unittest.TestCase):

    def test_task_completion(self):
        """Verify that calling mark_complete() actually changes the task's status."""
        task = Task(name="Test Task", category="test", duration=10, priority=3)
        self.assertFalse(task.completed)  # Initially not completed
        task.mark_complete()
        self.assertTrue(task.completed)  # After marking, should be completed

    def test_task_addition_to_pet(self):
        """Verify that adding a task to a Pet increases that pet's task count."""
        pet = Pet(name="Test Pet", species="dog", age=5)
        initial_count = len(pet.tasks)
        task = Task(name="New Task", category="test", duration=15, priority=2)
        pet.tasks.append(task)
        self.assertEqual(len(pet.tasks), initial_count + 1)

    # ============ SORTING CORRECTNESS TESTS ============

    def test_sort_tasks_by_priority_descending(self):
        """Verify tasks are sorted by priority in descending order."""
        owner = Owner(
            name="Alice",
            available_time={"morning": (8, 12)},
            preferences={"feeding": "high", "play": "low"}
        )
        pet = Pet(name="Fluffy", species="dog", age=3)
        
        # Create tasks with varying priorities
        task_low = Task(name="Play", category="play", duration=30, priority=1)
        task_mid = Task(name="Groom", category="grooming", duration=60, priority=2)
        task_high = Task(name="Feed", category="feeding", duration=15, priority=3)
        
        tasks = [task_low, task_mid, task_high]
        
        schedule = Schedule("2026-03-29", owner, pet)
        sorted_tasks = schedule.sort_tasks(tasks, owner.preferences)
        
        # Verify descending priority order
        self.assertEqual(sorted_tasks[0].priority, 3)
        self.assertEqual(sorted_tasks[1].priority, 2)
        self.assertEqual(sorted_tasks[2].priority, 1)

    def test_sort_tasks_by_preference_when_priority_tied(self):
        """Verify preference weight breaks ties when priorities are equal."""
        owner = Owner(
            name="Bob",
            available_time={"morning": (8, 12)},
            preferences={"feeding": "high", "play": "low", "grooming": "medium"}
        )
        pet = Pet(name="Max", species="cat", age=2)
        
        # Create tasks with same priority but different preference weights
        task_feeding = Task(name="Feed", category="feeding", duration=15, priority=2)
        task_play = Task(name="Play", category="play", duration=30, priority=2)
        task_grooming = Task(name="Groom", category="grooming", duration=60, priority=2)
        
        tasks = [task_play, task_grooming, task_feeding]  # Intentionally unordered
        
        schedule = Schedule("2026-03-29", owner, pet)
        sorted_tasks = schedule.sort_tasks(tasks, owner.preferences)
        
        # Should be: feeding (high=3), grooming (medium=2), play (low=1)
        self.assertEqual(sorted_tasks[0].category, "feeding")
        self.assertEqual(sorted_tasks[1].category, "grooming")
        self.assertEqual(sorted_tasks[2].category, "play")

    def test_sort_tasks_with_default_preference(self):
        """Verify tasks with missing preferences default to medium weight."""
        owner = Owner(
            name="Charlie",
            available_time={"morning": (8, 12)},
            preferences={"feeding": "high"}  # Only one preference
        )
        pet = Pet(name="Buddy", species="dog", age=4)
        
        task_feeding = Task(name="Feed", category="feeding", duration=15, priority=1)
        task_unknown = Task(name="Unknown", category="unknown_category", duration=30, priority=1)
        
        tasks = [task_unknown, task_feeding]
        
        schedule = Schedule("2026-03-29", owner, pet)
        sorted_tasks = schedule.sort_tasks(tasks, owner.preferences)
        
        # feeding (high=3) should come before unknown (default medium=2)
        self.assertEqual(sorted_tasks[0].category, "feeding")
        self.assertEqual(sorted_tasks[1].category, "unknown_category")

    def test_sort_empty_task_list(self):
        """Verify sorting an empty list doesn't crash."""
        owner = Owner(
            name="Diana",
            available_time={"morning": (8, 12)},
            preferences={"feeding": "high"}
        )
        pet = Pet(name="Luna", species="cat", age=1)
        
        schedule = Schedule("2026-03-29", owner, pet)
        sorted_tasks = schedule.sort_tasks([], owner.preferences)
        
        self.assertEqual(len(sorted_tasks), 0)

    # ============ RECURRENCE LOGIC TESTS ============

    def test_daily_task_recurrence_creates_next_day_task(self):
        """Verify marking a daily task complete creates a new task for the following day."""
        today = date.today()
        task = Task(
            name="Feed Daily",
            category="feeding",
            duration=15,
            priority=3,
            frequency="daily",
            due_date=today
        )
        
        next_task = task.mark_complete()
        
        # Verify original task is marked complete
        self.assertTrue(task.completed)
        
        # Verify new task is created
        self.assertIsNotNone(next_task)
        self.assertEqual(next_task.name, "Feed Daily")
        self.assertEqual(next_task.due_date, today + timedelta(days=1))
        self.assertFalse(next_task.completed)

    def test_weekly_task_recurrence_creates_next_week_task(self):
        """Verify marking a weekly task complete creates a new task for the following week."""
        today = date.today()
        task = Task(
            name="Bath Weekly",
            category="bathing",
            duration=60,
            priority=2,
            frequency="weekly",
            due_date=today
        )
        
        next_task = task.mark_complete()
        
        # Verify original task is marked complete
        self.assertTrue(task.completed)
        
        # Verify new task is created for next week
        self.assertIsNotNone(next_task)
        self.assertEqual(next_task.name, "Bath Weekly")
        self.assertEqual(next_task.due_date, today + timedelta(weeks=1))
        self.assertFalse(next_task.completed)

    def test_non_recurring_task_no_next_task(self):
        """Verify marking a non-recurring (frequency='none') task returns None."""
        task = Task(
            name="One-Time Event",
            category="event",
            duration=30,
            priority=1,
            frequency="none",
            due_date=date.today()
        )
        
        next_task = task.mark_complete()
        
        self.assertTrue(task.completed)
        self.assertIsNone(next_task)

    def test_recurring_task_without_due_date(self):
        """Verify recurrence works when due_date is initially None."""
        task = Task(
            name="Daily Task",
            category="feeding",
            duration=15,
            priority=3,
            frequency="daily",
            due_date=None  # No initial due date
        )
        
        next_task = task.mark_complete()
        
        self.assertTrue(task.completed)
        self.assertIsNotNone(next_task)
        # Should create task for today + 1 (starting from today since due_date was None)
        self.assertEqual(next_task.due_date, date.today() + timedelta(days=1))

    def test_recurrence_chain_multiple_completions(self):
        """Verify a recurring task can be completed multiple times in succession."""
        today = date.today()
        task = Task(
            name="Daily Feed",
            category="feeding",
            duration=15,
            priority=3,
            frequency="daily",
            due_date=today
        )
        
        # Complete 3 times in succession
        next1 = task.mark_complete()
        self.assertEqual(next1.due_date, today + timedelta(days=1))
        
        next2 = next1.mark_complete()
        self.assertEqual(next2.due_date, today + timedelta(days=2))
        
        next3 = next2.mark_complete()
        self.assertEqual(next3.due_date, today + timedelta(days=3))

    def test_recurrence_preserves_task_properties(self):
        """Verify all task properties are preserved in recurrence."""
        today = date.today()
        task = Task(
            name="Special Feed",
            category="feeding",
            duration=25,
            priority=3,
            frequency="daily",
            preferred_time="morning",
            pet_specific=True,
            due_date=today
        )
        
        next_task = task.mark_complete()
        
        # Verify all properties match except completed and due_date
        self.assertEqual(next_task.name, task.name)
        self.assertEqual(next_task.category, task.category)
        self.assertEqual(next_task.duration, task.duration)
        self.assertEqual(next_task.priority, task.priority)
        self.assertEqual(next_task.frequency, task.frequency)
        self.assertEqual(next_task.preferred_time, task.preferred_time)
        self.assertEqual(next_task.pet_specific, task.pet_specific)

    # ============ CONFLICT DETECTION TESTS ============

    def test_detect_overlapping_tasks(self):
        """Verify scheduler detects overlapping task times."""
        owner = Owner(
            name="Eve",
            available_time={"morning": (8, 12), "afternoon": (14, 18)},
            preferences={}
        )
        pets = [Pet(name="Fluffy", species="dog", age=3), Pet(name="Whiskers", species="cat", age=2)]
        owner.pets = pets
        
        task1 = Task(name="Dog Walk", category="exercise", duration=30, priority=2)
        task2 = Task(name="Cat Play", category="play", duration=45, priority=2)
        
        pets[0].tasks.append(task1)
        pets[1].tasks.append(task2)
        
        schedule = Schedule("2026-03-29", owner, pets[0])
        schedule.add_task(task1, "09:00", "Morning walk")
        schedule.add_task(task2, "09:15", "Afternoon play")  # Overlaps with task1
        
        conflicts = schedule.detect_scheduling_conflicts()
        
        # Should detect at least one conflict
        self.assertGreater(len(conflicts), 0)
        self.assertEqual(conflicts[0]["task1"], "Dog Walk")
        self.assertEqual(conflicts[0]["task2"], "Cat Play")

    def test_no_conflict_for_adjacent_tasks(self):
        """Verify adjacent (non-overlapping) tasks are not flagged as conflicts."""
        owner = Owner(
            name="Frank",
            available_time={"morning": (8, 12)},
            preferences={}
        )
        pet = Pet(name="Buddy", species="dog", age=4)
        owner.pets.append(pet)
        
        task1 = Task(name="Feed", category="feeding", duration=30, priority=2)  # 08:00-08:30
        task2 = Task(name="Walk", category="exercise", duration=30, priority=2)  # 08:30-09:00
        
        pet.tasks.extend([task1, task2])
        
        schedule = Schedule("2026-03-29", owner, pet)
        schedule.add_task(task1, "08:00", "Morning feed")
        schedule.add_task(task2, "08:30", "Morning walk")
        
        conflicts = schedule.detect_scheduling_conflicts()
        
        # No conflict—task2 starts exactly when task1 ends
        self.assertEqual(len(conflicts), 0)

    def test_conflict_with_exact_overlap(self):
        """Verify exact time overlaps are detected."""
        owner = Owner(
            name="Grace",
            available_time={"all_day": (0, 24)},
            preferences={}
        )
        pet = Pet(name="Fido", species="dog", age=5)
        owner.pets.append(pet)
        
        task1 = Task(name="Activity1", category="play", duration=60, priority=1)
        task2 = Task(name="Activity2", category="exercise", duration=60, priority=1)
        
        pet.tasks.extend([task1, task2])
        
        schedule = Schedule("2026-03-29", owner, pet)
        schedule.add_task(task1, "10:00", "First activity")
        schedule.add_task(task2, "10:00", "Second activity")  # Same start time
        
        conflicts = schedule.detect_scheduling_conflicts()
        
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0]["task1"], "Activity1")
        self.assertEqual(conflicts[0]["task2"], "Activity2")

    def test_no_conflicts_single_task(self):
        """Verify schedule with single task has no conflicts."""
        owner = Owner(
            name="Henry",
            available_time={"morning": (8, 12)},
            preferences={}
        )
        pet = Pet(name="Rex", species="dog", age=2)
        owner.pets.append(pet)
        
        task = Task(name="Feed", category="feeding", duration=30, priority=3)
        pet.tasks.append(task)
        
        schedule = Schedule("2026-03-29", owner, pet)
        schedule.add_task(task, "09:00", "Morning feed")
        
        conflicts = schedule.detect_scheduling_conflicts()
        
        self.assertEqual(len(conflicts), 0)

    def test_partial_overlap_detected(self):
        """Verify partial overlaps (not full containment) are detected."""
        owner = Owner(
            name="Iris",
            available_time={"all_day": (0, 24)},
            preferences={}
        )
        pet = Pet(name="Bella", species="cat", age=3)
        owner.pets.append(pet)
        
        task1 = Task(name="Task1", category="activity", duration=60, priority=1)  # 10:00-11:00
        task2 = Task(name="Task2", category="activity", duration=60, priority=1)  # 10:30-11:30
        
        pet.tasks.extend([task1, task2])
        
        schedule = Schedule("2026-03-29", owner, pet)
        schedule.add_task(task1, "10:00", "First task")
        schedule.add_task(task2, "10:30", "Overlapping task")
        
        conflicts = schedule.detect_scheduling_conflicts()
        
        self.assertEqual(len(conflicts), 1)


if __name__ == '__main__':
    unittest.main()
