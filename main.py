from pawpal_system import Pet, Owner, Task, Schedule

# Create pets
pet1 = Pet(name="Mochi", species="dog", age=3, breed="Shih Tzu")
pet2 = Pet(name="Whiskers", species="cat", age=2)

# Create tasks (out of meaningful order intentionally)
task1 = Task(name="Morning walk", category="walking", duration=30, priority=5, preferred_time="morning")
task2 = Task(name="Feeding", category="feeding", duration=10, priority=4, preferred_time="morning")
task3 = Task(name="Playtime", category="enrichment", duration=20, priority=3, preferred_time="afternoon")
task4 = Task(name="Evening grooming", category="grooming", duration=25, priority=2, preferred_time="evening")
task5 = Task(name="Medication", category="meds", duration=5, priority=5, preferred_time="morning")
# Two overlapping high-priority tasks to test conflict detection
task6 = Task(name="Vet appointment", category="meds", duration=40, priority=5, preferred_time="morning")
task7 = Task(name="Training session", category="enrichment", duration=35, priority=5, preferred_time="morning")

# Add tasks to pets out of order (append sequenced differently than priority)
pet1.tasks.append(task2)
pet1.tasks.append(task1)
pet1.tasks.append(task4)
pet1.tasks.append(task6)  # Add overlapping task to Mochi
pet2.tasks.append(task3)
pet2.tasks.append(task5)
pet2.tasks.append(task7)  # Add overlapping task to Whiskers

# Mark one task complete to exercise filter behavior
task2.mark_complete()  # Feeding is done already

# Create owner
owner = Owner(
    name="Jordan",
    available_time={"morning": (8, 12), "afternoon": (13, 17)},
    preferences={"walking": "high", "feeding": "high", "enrichment": "medium"}
)
owner.pets.append(pet1)
owner.pets.append(pet2)

# Generate today's schedule with warning detection
today = "2024-10-01"
schedule, warnings = Schedule.generate_plan_with_warnings(today, owner)

# Print the schedule
print("Today's Schedule:")
print(schedule.explain_plan())

# Print any detected warnings/conflicts
if warnings:
    print("\n⚠️  SCHEDULING CONFLICTS DETECTED:")
    for warning in warnings:
        print(f"  {warning}")
else:
    print("\n✅ No scheduling conflicts detected.")

print("\nDetailed Plan:")
print(f"{'Task':<20} {'Start':<10} {'End':<10} {'Reason'}")
print("-" * 80)
for entry in schedule.get_plan_summary():
    task_name = entry['task'].name[:19]  # Truncate if too long
    print(f"{task_name:<20} {entry['start_time']:<10} {entry['end_time']:<10} {entry['reason']}")
print(f"\nTotal time: {schedule.total_time} minutes")

# Filter examples using new Owner method
print("\nAll pending tasks:")
for t in owner.filter_tasks(completed=False):
    print(f"- {t.name} (pet: {next((p.name for p in owner.pets if t in p.tasks), 'unknown')}, priority {t.priority})")

print("\nTasks for Mochi:")
for t in owner.filter_tasks(pet_name='Mochi'):
    print(f"- {t.name} (completed={t.completed}, priority {t.priority})")

print("\nTasks sorted by scheduler internal order, even when added out of order:")
sorted_tasks = schedule.sort_tasks(owner.get_all_tasks(), owner.preferences)
for t in sorted_tasks:
    print(f"- {t.name} (priority {t.priority}, completed={t.completed})")
