# PawPal+ Project Reflection

## 1. System Design

- A user should be able to enter basic pet info
- A user should be able to look at a generated schedule/plan 
- A user should be able to consider constraints like time and
**a. Initial design**

The initial UML design was a class diagram created using Mermaid to model the pet care planning system. It used object-oriented principles, and had data classes (Pet, Owner, Task) and a logic class (Schedule).

Classes:
- Pet: Represents the pet with attributes like name, species, age, and special needs. Responsibilities include providing pet information and checking for specific needs that might affect task selection.
- Owner: Represents the pet owner with availability time slots and preferences. Responsibilities include managing owned pets and providing preference weights for task prioritization.
- Task: Represents individual care tasks with details like duration, priority, and preferred time. Responsibilities include determining if a task is due and providing descriptions.
- Schedule: Combines planning and scheduling logic. Responsibilities include generating a daily plan based on owner/pet/tasks, sorting tasks by priority/preferences, fitting them into available time slots, and explaining the plan with reasons.

**b. Design changes**

Yes, the design changed during implementation. The "Schedule.generate_plan" method was changed from an instance method to a classmethod to act as something  creating "Schedule" instances. This improved the skeleton by making it clearer and it now produces a new plan object without requiring an existing schedule.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
