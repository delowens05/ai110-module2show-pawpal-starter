# PawPal+ Project Reflection

## 1. System Design

- A user should be able to enter basic pet info
- A user should be able to look at a generated schedule/plan 
- A user should be able to consider constraints like time and priorty 
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

The scheduler considers three main constraints: available time slots (morning, afternoon, evening windows), task priority (1-5 scale where 5 is highest), and owner preferences for task categories (high/medium/low). The scheduler weights priority highest, then owner preference, then fits tasks into the earliest available slot. This ranking was chosen because urgent tasks (high priority) should take precedence, but owner preferences (e.g., "I prefer walking in the morning") should guide placement when multiple high-priority slots exist.

**b. Tradeoffs**

One tradeoff is using "first-fit" scheduling instead of "best-fit" bin-packing. For a daily pet schedule with typically 3-10 tasks, first-fit is reasonable because schedules are small enough that the speed gain outweighs wasted time. Additionally, the non-blocking conflict detection (warnings instead of hard failures) trades scheduling completeness for user conflicts are flagged but don't prevent plan generation, allowing owners to review and manually adjust rather than getting blocked.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI tools to help design my UML diagram with Mermaid.js, especially for brainstorming a more effective way to structure and visualize my system. I also relied on AI for debugging when my tests failed, helping me quickly identify and fix issues in my code. In addition, I used it to refactor some of my methods to improve efficiency, particularly with sorting logic. I also used AI to make my readme and reflection more structured when explaining key ideas, and the most helpful prompts were brainstorming questions and requests to optimize or rewrite code.

**b. Judgment and verification**

I did not accept an AI suggestion as-is was when I asked for help optimizing a scheduling algorithm. While the AI solution may have improved performance, it made the code much harder to read and understand, which I felt was not worth it. To evaluate the suggestion, I reviewed the logic carefully and considered both efficiency and code clarity, ultimately deciding to prioritize maintainability. I verified my decision by ensuring my original version still worked correctly and was easier to follow and debug.

---

## 4. Testing and Verification

**a. What you tested**

I tested behaviors like task completion, adding tasks to pets, sorting tasks by priority and preferences, recurrence logic for daily and weekly tasks, and detecting scheduling conflicts. These tests were important because they make sure the core features of the system work correctly, especially more complex logic like sorting and time overlap detection. They also helped catch edge cases, like empty task lists or recurring tasks without due dates, so the system is more reliable.
'
**b. Confidence**

I’m pretyy confident that my scheduler works correctly because I tested behaviors like sorting, recurrence, and conflict detection across different scenarios. If I had more time, I would test additional edge cases like missing data or conflicting preferences, to make sure the system stays stable in all situations.

## 5. Reflection

**a. What went well**

- I think I'm most satifised with how organized the app is and how user friendly it is. I am alos very happy with the optimaized algoritms used in it.

**b. What you would improve**

- I'D probably try to see if I could make more than 4 classes so the diagram won't be as messy, I can see if maybe i can make a mroe effcient diagram and design.

**c. Key takeaway**

- I learned that class design is not a one, two or three step process. It is through constant iteration and testing that you get more effcient and valuable results.
