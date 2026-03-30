import streamlit as st
from pawpal_system import Owner, Pet, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner + Pets")
if "owner" not in st.session_state:
    st.session_state.owner = None
if "pets" not in st.session_state:
    st.session_state.pets = []
if "tasks" not in st.session_state:
    st.session_state.tasks = []

owner_name = st.text_input("Owner name", value="Jordan")
owner_pref_walking = st.selectbox("Walking preference", ["high", "medium", "low"], index=0)
owner_pref_feeding = st.selectbox("Feeding preference", ["high", "medium", "low"], index=0)

st.markdown("### Add a pet")
pet_name = st.text_input("Pet name", value="Mochi")
pet_species = st.selectbox("Species", ["dog", "cat", "other"])
pet_age = st.number_input("Age", min_value=0, max_value=30, value=3)

if st.button("Add pet"):
    new_pet = Pet(name=pet_name, species=pet_species, age=int(pet_age))
    st.session_state.pets.append(new_pet)
    st.success(f"Added pet: {new_pet.name}")

if st.session_state.pets:
    st.write("Current pets:")
    for idx, p in enumerate(st.session_state.pets, start=1):
        st.write(f"{idx}. {p.name} ({p.species}, age {p.age})")
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.markdown("### Add a task")
if st.session_state.pets:
    current_pet_names = [p.name for p in st.session_state.pets]
    selected_pet_name = st.selectbox("Select pet", current_pet_names)
    task_title = st.text_input("Task title", value="Morning walk")
    task_category = st.selectbox("Category", ["walking", "feeding", "meds", "enrichment", "grooming"])
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    priority = st.selectbox("Priority", [1, 2, 3, 4, 5], index=4)
    preferred_time = st.selectbox("Preferred time", ["morning", "afternoon", "evening", "anytime"])

    if st.button("Add task"):
        task = Task(
            name=task_title,
            category=task_category,
            duration=int(duration),
            priority=int(priority),
            preferred_time=preferred_time,
        )
        pet = next((p for p in st.session_state.pets if p.name == selected_pet_name), None)
        if pet is not None:
            pet.tasks.append(task)
            st.session_state.tasks.append(task)
            st.success(f"Added task to {pet.name}: {task.title if hasattr(task,'title') else task.name}")
else:
    st.info("Add at least one pet before adding tasks.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a schedule from pets and tasks.")

if st.button("Generate schedule"):
    if not st.session_state.pets:
        st.error("No pets available. Add a pet first.")
    else:
        owner = Owner(
            name=owner_name,
            available_time={"morning": (8, 12), "afternoon": (13, 17), "evening": (17, 21)},
            preferences={"walking": owner_pref_walking, "feeding": owner_pref_feeding},
            pets=st.session_state.pets,
        )
        st.session_state.owner = owner
        schedule = Schedule.generate_plan(date="today", owner=owner)
        st.markdown("### Today's Schedule")
        st.write(schedule.explain_plan())

        if schedule.get_plan_summary():
            st.table([
                {
                    "Task": e["task"].name,
                    "Start": e["start_time"],
                    "End": e["end_time"],
                    "Reason": e["reason"],
                }
                for e in schedule.get_plan_summary()
            ])
        else:
            st.info("No tasks fit in the available slots.")

