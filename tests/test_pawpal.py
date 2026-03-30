import unittest
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


if __name__ == '__main__':
    unittest.main()
