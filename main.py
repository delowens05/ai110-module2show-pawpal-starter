from pawpal_system import Pet, Owner, Task, Schedule

# Create pets
pet1 = Pet(name="Mochi", species="dog", age=3, breed="Shih Tzu")
pet2 = Pet(name="Whiskers", species="cat", age=2)

# Create tasks
task1 = Task(name="Morning walk", category="walking", duration=30, priority=5, preferred_time="morning")
task2 = Task(name="Feeding", category="feeding", duration=10, priority=4, preferred_time="morning")
task3 = Task(name="Playtime", category="enrichment", duration=20, priority=3, preferred_time="afternoon")

# Add tasks to pets
pet1.tasks.append(task1)
pet1.tasks.append(task2)
pet2.tasks.append(task3)

# Create owner
owner = Owner(
    name="Jordan",
    available_time={"morning": (8, 12), "afternoon": (13, 17)},
    preferences={"walking": "high", "feeding": "high", "enrichment": "medium"}
)
owner.pets.append(pet1)
owner.pets.append(pet2)

# Generate today's schedule
today = "2024-10-01"
schedule = Schedule.generate_plan(today, owner)

# Print the schedule
print("Today's Schedule:")
print(schedule.explain_plan())
print("\nDetailed Plan:")
print(f"{'Task':<20} {'Start':<10} {'End':<10} {'Reason'}")
print("-" * 80)
for entry in schedule.get_plan_summary():
    task_name = entry['task'].name[:19]  # Truncate if too long
    print(f"{task_name:<20} {entry['start_time']:<10} {entry['end_time']:<10} {entry['reason']}")
print(f"\nTotal time: {schedule.total_time} minutes")
