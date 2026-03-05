from sqlalchemy.orm import Session
from sqlalchemy import func

from models.interview_session import InterviewSession
from models.question import Question


def create_session(db: Session, user_id: int, interview_type: str, topic: str, difficulty: str):
    """Create and return a new InterviewSession."""
    session = InterviewSession(
        user_id=user_id,
        interview_type=interview_type,
        topic=topic,
        difficulty=difficulty,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_random_question(db: Session, topic: str, difficulty: str):
    """Return a random Question matching the given topic and difficulty."""
    question = (
        db.query(Question)
        .filter(Question.topic == topic, Question.difficulty == difficulty)
        .order_by(func.random())
        .first()
    )
    return question


def seed_questions(db: Session):
    """Seed 25 sample questions into the database if the table is empty."""
    existing = db.query(Question).count()
    if existing > 0:
        return {"message": f"Questions already seeded ({existing} found). Skipping."}

    sample_questions = [
        # Arrays
        Question(topic="arrays", difficulty="easy", type="technical",
                 question_text="What is an array and how does it differ from a linked list?",
                 ideal_answer="An array is a contiguous block of memory with O(1) random access, while a linked list uses nodes with pointers and offers O(1) insertion/deletion."),
        Question(topic="arrays", difficulty="medium", type="technical",
                 question_text="How would you find the two numbers in an array that add up to a target sum?",
                 ideal_answer="Use a hash map to store complements. For each element, check if target - element exists in the map. O(n) time, O(n) space."),
        Question(topic="arrays", difficulty="hard", type="technical",
                 question_text="Explain how to find the median of two sorted arrays in O(log(min(m,n))) time.",
                 ideal_answer="Use binary search on the smaller array to partition both arrays such that left halves contain the smaller elements."),

        # Trees
        Question(topic="trees", difficulty="easy", type="technical",
                 question_text="What is a binary search tree (BST)?",
                 ideal_answer="A BST is a binary tree where the left child is smaller and the right child is larger than the parent node."),
        Question(topic="trees", difficulty="medium", type="technical",
                 question_text="How do you check if a binary tree is balanced?",
                 ideal_answer="Recursively compute the height of left and right subtrees; a tree is balanced if the height difference is at most 1 for every node."),
        Question(topic="trees", difficulty="hard", type="technical",
                 question_text="Explain how to serialize and deserialize a binary tree.",
                 ideal_answer="Use preorder traversal with null markers for serialization. Deserialize by reading tokens and reconstructing nodes recursively."),

        # Sorting
        Question(topic="sorting", difficulty="easy", type="technical",
                 question_text="Explain the bubble sort algorithm.",
                 ideal_answer="Bubble sort repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order. O(n^2) average."),
        Question(topic="sorting", difficulty="medium", type="technical",
                 question_text="What is the time complexity of merge sort and how does it work?",
                 ideal_answer="Merge sort divides the array into halves, recursively sorts them, and merges the sorted halves. O(n log n) in all cases."),
        Question(topic="sorting", difficulty="hard", type="technical",
                 question_text="How does quicksort perform in the worst case and how can you mitigate it?",
                 ideal_answer="Worst case is O(n^2) when the pivot is always the smallest/largest element. Use randomized pivot or median-of-three to mitigate."),
        Question(topic="sorting", difficulty="medium", type="technical",
                 question_text="Compare merge sort and quicksort in terms of space complexity.",
                 ideal_answer="Merge sort uses O(n) extra space for merging, while quicksort can be done in-place with O(log n) stack space."),

        # Dynamic Programming
        Question(topic="dp", difficulty="easy", type="technical",
                 question_text="What is dynamic programming and when should you use it?",
                 ideal_answer="DP solves problems by breaking them into overlapping subproblems and storing results to avoid recomputation. Use when optimal substructure and overlapping subproblems exist."),
        Question(topic="dp", difficulty="medium", type="technical",
                 question_text="How do you solve the 0/1 knapsack problem using dynamic programming?",
                 ideal_answer="Build a 2D table dp[i][w] representing max value using first i items with capacity w. For each item, choose to include or exclude it."),
        Question(topic="dp", difficulty="hard", type="technical",
                 question_text="Explain the longest common subsequence (LCS) problem and its DP solution.",
                 ideal_answer="LCS finds the longest subsequence common to two sequences. Use a 2D table where dp[i][j] = dp[i-1][j-1]+1 if characters match, else max(dp[i-1][j], dp[i][j-1])."),
        Question(topic="dp", difficulty="medium", type="technical",
                 question_text="How would you find the minimum number of coins to make a given amount?",
                 ideal_answer="Use dp[i] = min coins for amount i. For each coin, dp[i] = min(dp[i], dp[i-coin]+1). Initialize dp[0]=0, others=infinity."),

        # OOPs
        Question(topic="oops", difficulty="easy", type="technical",
                 question_text="What are the four pillars of Object-Oriented Programming?",
                 ideal_answer="Encapsulation, Abstraction, Inheritance, and Polymorphism."),
        Question(topic="oops", difficulty="medium", type="technical",
                 question_text="Explain the difference between an abstract class and an interface.",
                 ideal_answer="An abstract class can have implementation and state; an interface only declares method signatures (in most languages). A class can implement multiple interfaces but inherit from one abstract class."),
        Question(topic="oops", difficulty="hard", type="technical",
                 question_text="What is the SOLID principle? Explain each letter briefly.",
                 ideal_answer="S-Single Responsibility, O-Open/Closed, L-Liskov Substitution, I-Interface Segregation, D-Dependency Inversion. Each guides maintainable OOP design."),
        Question(topic="oops", difficulty="easy", type="technical",
                 question_text="What is polymorphism? Give an example.",
                 ideal_answer="Polymorphism allows objects of different classes to be treated as instances of a common parent class. E.g., a Shape class with draw() overridden by Circle and Rectangle."),

        # Behavioral
        Question(topic="behavioral", difficulty="easy", type="hr",
                 question_text="Tell me about yourself.",
                 ideal_answer="Provide a concise summary of your background, key skills, and what you are looking for in your next role."),
        Question(topic="behavioral", difficulty="medium", type="hr",
                 question_text="Describe a time you faced a challenging deadline. How did you handle it?",
                 ideal_answer="Use the STAR method: describe the Situation, Task, Action you took, and the Result achieved."),
        Question(topic="behavioral", difficulty="easy", type="hr",
                 question_text="Why do you want to work at this company?",
                 ideal_answer="Research the company values, products, and culture. Align your skills and interests with the company's mission."),
        Question(topic="behavioral", difficulty="medium", type="hr",
                 question_text="Give an example of a time you had a conflict with a team member.",
                 ideal_answer="Describe the conflict objectively, explain how you resolved it through communication, and share the positive outcome."),
        Question(topic="behavioral", difficulty="hard", type="hr",
                 question_text="Describe a situation where you had to make a decision with incomplete information.",
                 ideal_answer="Explain the context, how you gathered available data, the decision-making framework you used, and the outcome."),
        Question(topic="behavioral", difficulty="easy", type="hr",
                 question_text="What are your strengths and weaknesses?",
                 ideal_answer="Mention genuine strengths relevant to the role and a real weakness you are actively working to improve."),
        Question(topic="behavioral", difficulty="hard", type="hr",
                 question_text="Tell me about a time you failed and what you learned from it.",
                 ideal_answer="Describe a genuine failure, take responsibility, explain the lessons learned, and how you applied them going forward."),
    ]

    db.add_all(sample_questions)
    db.commit()
    return {"message": f"Successfully seeded {len(sample_questions)} questions."}