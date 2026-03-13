"""
seed_v2.py — Phase 14: Question Bank Expansion
Adds ~207 questions to reach target distribution:
DSA=120, OOPS=40, DBMS=40, OS=40, System Design=30, ML=40, Behavioral=30
"""
import psycopg2

DB_URL = "postgresql://postgres:admin123@localhost:5432/interview_db"

def run():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    def add(subject_id, topic_id, subtopic_id, title, difficulty, qtype, question_text, ideal_answer, tags=None, companies=None):
        cur.execute("""
            INSERT INTO questions (subject_id, topic_id, subtopic_id, title, difficulty, type, question_text, ideal_answer, tags, companies)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (subject_id, topic_id, subtopic_id, title, difficulty, qtype,
              question_text, ideal_answer,
              tags or [], companies or []))

    # =========================================================
    # DSA — subject_id=1
    # =========================================================

    # Arrays > Prefix Sum (topic=1, sub=2)
    add(1,1,2,"Range Sum Query","medium","coding",
        "Given an array, answer multiple range sum queries [l, r] efficiently using prefix sums.",
        "Build prefix[] where prefix[i] = prefix[i-1] + arr[i-1]. Range sum [l,r] = prefix[r+1] - prefix[l]. O(n) build, O(1) query.",
        ["prefix_sum","arrays"],["Amazon","Google"])
    add(1,1,2,"Subarray Sum Equals K","medium","coding",
        "Count subarrays with sum equal to K using prefix sum and hashmap.",
        "Use hashmap {prefix_sum: count}. For each i, if (current_sum - K) exists in map, add its count. Running sum technique gives O(n) time.",
        ["prefix_sum","hashmap"],["Facebook","Uber"])
    add(1,1,2,"Product of Array Except Self","medium","coding",
        "Return array where each element is product of all other elements. No division allowed.",
        "Two passes: left prefix products and right suffix products. result[i] = left[i] * right[i]. O(n) time, O(1) extra space.",
        ["prefix_sum","arrays"],["Amazon","Microsoft"])

    # Arrays > Kadane (topic=1, sub=3)
    add(1,1,3,"Maximum Product Subarray","medium","coding",
        "Find the contiguous subarray with the largest product.",
        "Track both max and min running products (negative * negative = positive). Update both at each step. O(n) time.",
        ["kadane","dp"],["LeetCode","Google"])
    add(1,1,3,"Circular Subarray Maximum Sum","hard","coding",
        "Find maximum sum of a subarray in a circular array.",
        "Either max is non-wrapping (Kadane's on full array) or wrapping (total_sum - min_subarray_sum). Take max of both, handle all-negative case.",
        ["kadane","circular"],["Amazon"])
    add(1,1,3,"Kadane's Algorithm Explained","easy","conceptual",
        "Explain Kadane's algorithm. What problem does it solve and what is its time complexity?",
        "Kadane's finds maximum subarray sum in O(n). Maintains running sum; if it goes negative, reset to 0. Track global max. Classic DP where local_max[i] = max(arr[i], local_max[i-1]+arr[i]).",
        ["kadane","dp"],["Interview"])

    # Arrays > Dutch Flag (topic=1, sub=6)
    add(1,1,6,"Sort Colors (Dutch Flag)","medium","coding",
        "Sort an array of 0s, 1s, 2s in-place in one pass.",
        "Three pointers: low=0, mid=0, high=n-1. If arr[mid]==0 swap with low and advance both. If 1 advance mid. If 2 swap with high and decrement high. O(n) one pass.",
        ["dutch_flag","two_pointers"],["Google","Microsoft"])
    add(1,1,6,"Partition Array Around Pivot","medium","coding",
        "Partition array so elements < pivot come first, equal next, greater last.",
        "Dutch flag variant with 3-way partition. Use low/mid/high pointers. This is the partition step in 3-way quicksort. O(n) time, O(1) space.",
        ["dutch_flag","sorting"],["Amazon"])
    add(1,1,6,"Segregate Even and Odd","easy","coding",
        "Move all even numbers to front and odd to back in O(n) time.",
        "Two pointer approach: left from start, right from end. Swap when left is odd and right is even. Similar to Dutch flag with 2 partitions.",
        ["dutch_flag","two_pointers"],["Infosys"])

    # Arrays > Cyclic Sort (topic=1, sub=9)
    add(1,1,9,"Find All Missing Numbers","medium","coding",
        "Given array of n integers in range [1,n], find all missing numbers.",
        "Cyclic sort: place each number at index num-1. After sorting, indices where arr[i]!=i+1 are missing. O(n) time, O(1) space.",
        ["cyclic_sort","arrays"],["Amazon","Facebook"])
    add(1,1,9,"Find Duplicate and Missing","hard","coding",
        "Array contains n numbers from 1 to n with one duplicate and one missing. Find both.",
        "Cyclic sort to place numbers at correct indices. Then scan: index where arr[i]!=i+1 gives duplicate (arr[i]) and missing (i+1).",
        ["cyclic_sort"],["Google"])
    add(1,1,9,"Cyclic Sort Explained","easy","conceptual",
        "Explain cyclic sort. When is it useful and what is its complexity?",
        "Cyclic sort works on arrays with numbers in range [1,n] or [0,n-1]. Place each number at its correct index by swapping. O(n) time, O(1) space. Useful for finding missing/duplicate numbers.",
        ["cyclic_sort"],["Interview"])

    # Arrays > Intervals (topic=1, sub=8)
    add(1,1,8,"Merge Overlapping Intervals","medium","coding",
        "Given list of intervals, merge all overlapping ones.",
        "Sort by start time. Iterate: if current.start <= last_merged.end, merge by extending end. Otherwise add new interval. O(n log n).",
        ["intervals","sorting"],["Google","Facebook"])
    add(1,1,8,"Insert Interval","medium","coding",
        "Insert a new interval into sorted non-overlapping intervals and merge if needed.",
        "Three phases: add all intervals ending before new start, merge overlapping with new interval, add remaining. O(n) time.",
        ["intervals"],["Microsoft"])
    add(1,1,8,"Meeting Rooms II","medium","coding",
        "Find minimum number of conference rooms required for given meeting times.",
        "Sort by start. Use min-heap of end times. For each meeting, if earliest ending room is free (heap.min <= start), reuse it. Else add new room. Answer is heap size.",
        ["intervals","heap"],["Amazon","Airbnb"])

    # Arrays > Rotation (topic=1, sub=5)
    add(1,1,5,"Find Minimum in Rotated Sorted Array","medium","coding",
        "Find minimum element in a rotated sorted array in O(log n).",
        "Binary search: if mid > right, minimum is in right half. Else in left half (including mid). O(log n).",
        ["rotation","binary_search"],["Amazon","Microsoft"])
    add(1,1,5,"Search in Rotated Sorted Array","medium","coding",
        "Search for target in a rotated sorted array in O(log n).",
        "Binary search with rotation check: determine which half is sorted. If target in sorted half, search there. Else search other half. O(log n).",
        ["rotation","binary_search"],["Google","Facebook"])

    # Arrays > Two Pointers (topic=1, sub=4)
    add(1,1,4,"3Sum Problem","medium","coding",
        "Find all unique triplets in array that sum to zero.",
        "Sort array. For each element, use two pointers for the remaining. Skip duplicates. O(n²) time.",
        ["two_pointers","sorting"],["Amazon","Google"])
    add(1,1,4,"Container With Most Water","medium","coding",
        "Find two lines that together with x-axis forms container holding most water.",
        "Two pointers from both ends. Move pointer with smaller height inward (moving larger can only decrease area). O(n).",
        ["two_pointers"],["Amazon","Facebook"])

    # Arrays > Matrix (topic=1, sub=7)
    add(1,1,7,"Rotate Matrix 90 Degrees","medium","coding",
        "Rotate an NxN matrix 90 degrees clockwise in-place.",
        "Transpose (swap arr[i][j] and arr[j][i]) then reverse each row. O(n²) time, O(1) space.",
        ["matrix"],["Amazon","Microsoft"])
    add(1,1,7,"Spiral Order Matrix Traversal","medium","coding",
        "Return all elements of a matrix in spiral order.",
        "Maintain top, bottom, left, right boundaries. Traverse right, down, left, up, shrinking boundaries each time. O(m*n).",
        ["matrix"],["Google"])

    # Arrays > Binary Search on Array (topic=1, sub=10)
    add(1,1,10,"Find Peak Element","medium","coding",
        "Find a peak element (greater than neighbors) in O(log n).",
        "Binary search: if arr[mid] < arr[mid+1], peak is in right half. Else in left half. O(log n).",
        ["binary_search"],["Google","Facebook"])
    add(1,1,10,"Kth Largest in Unsorted Array","medium","coding",
        "Find kth largest element using quickselect algorithm.",
        "Quickselect: partition around pivot. If pivot index == k-1, found. If larger, search left. Else search right. O(n) average.",
        ["binary_search","sorting"],["Amazon"])

    # Arrays > Expert (topic=1, sub=11)
    add(1,1,11,"Trapping Rain Water","hard","coding",
        "Calculate how much water can be trapped between buildings.",
        "Two pointer: track leftMax and rightMax. If leftMax < rightMax, water = leftMax - arr[left], else rightMax - arr[right]. O(n) time O(1) space.",
        ["arrays","two_pointers"],["Amazon","Google"])
    add(1,1,11,"Largest Rectangle in Histogram","hard","coding",
        "Find the largest rectangle area in a histogram.",
        "Monotonic stack: push indices of increasing heights. When smaller height found, pop and calculate area using stored height and current width. O(n).",
        ["stack","arrays"],["Google","Uber"])
    add(1,1,11,"Sliding Window Maximum","hard","coding",
        "Find maximum in each sliding window of size k.",
        "Deque-based: maintain indices of decreasing elements. Front is always max. Remove front when out of window, remove from back when smaller. O(n).",
        ["sliding_window","deque"],["Amazon","Microsoft"])

    # Linked List > LRU (topic=3, sub=27)
    add(1,3,27,"LRU Cache Implementation","hard","coding",
        "Implement an LRU cache with O(1) get and put operations.",
        "Combine HashMap + Doubly Linked List. Map stores key→node. On get/put, move node to front (most recent). On capacity exceeded, remove tail (least recent). O(1) both ops.",
        ["lru_cache","linked_list","hashmap"],["Amazon","Google","Microsoft"])
    add(1,3,27,"LFU Cache Implementation","hard","coding",
        "Implement a Least Frequently Used (LFU) cache.",
        "Track frequency of each key. Use HashMap<freq, DoublyLinkedList> + HashMap<key, node>. On access, move node to next frequency bucket. On eviction, remove from min-frequency bucket.",
        ["lru_cache","design"],["Facebook"])
    add(1,3,27,"Design Cache with TTL","hard","coding",
        "Design a cache that supports TTL (time-to-live) expiration.",
        "Extend LRU with expiry timestamps. On get, check if expired and evict if so. Background thread or lazy eviction on access. Priority queue for TTL ordering.",
        ["lru_cache","design"],["Uber"])

    # DP > Expert (topic=18, sub=84)
    add(1,18,84,"Burst Balloons","hard","coding",
        "Given balloons with values, find max coins from bursting them optimally.",
        "Interval DP: dp[i][j] = max coins for balloons i..j. Try each k as last balloon to burst. dp[i][j] = max(dp[i][k-1] + val[i-1]*val[k]*val[j+1] + dp[k+1][j]). O(n³).",
        ["dp","interval_dp"],["Google"])
    add(1,18,84,"Regular Expression Matching","hard","coding",
        "Implement regex matching with '.' and '*' operators.",
        "2D DP: dp[i][j] = pattern[:j] matches string[:i]. For '*': dp[i][j] = dp[i][j-2] (zero occurrences) OR (pattern[j-1] matches s[i] AND dp[i-1][j]). O(m*n).",
        ["dp","strings"],["Facebook","Google"])
    add(1,18,84,"Minimum Edit Distance","hard","coding",
        "Find minimum edit distance (Levenshtein distance) between two strings.",
        "2D DP: dp[i][j] = min edits to convert word1[:i] to word2[:j]. If chars match, dp[i][j]=dp[i-1][j-1]. Else min(insert, delete, replace) + 1. O(m*n).",
        ["dp","strings"],["Amazon","Microsoft"])

    # Graphs > Shortest Path (topic=16, sub=74)
    add(1,16,74,"Dijkstra's Algorithm","hard","coding",
        "Find shortest path from source to all nodes in a weighted graph.",
        "Min-heap + distances array. Start with source dist=0. Relax neighbors: if dist[u]+w < dist[v], update and push to heap. O((V+E) log V).",
        ["graphs","shortest_path"],["Google","Amazon"])
    add(1,16,74,"Bellman-Ford Algorithm","hard","coding",
        "Find shortest path in a graph that may have negative weight edges.",
        "Relax all edges V-1 times. If any edge can still be relaxed after V-1 rounds, negative cycle exists. O(V*E). Handles negatives unlike Dijkstra.",
        ["graphs","shortest_path"],["Amazon"])
    add(1,16,74,"Floyd-Warshall All Pairs","hard","coding",
        "Find shortest paths between all pairs of vertices.",
        "3D DP: dist[k][i][j] = shortest i→j using only nodes 0..k. Recurrence: dist[k][i][j] = min(dist[k-1][i][j], dist[k-1][i][k]+dist[k-1][k][j]). O(V³).",
        ["graphs","dp"],["Google"])

    # Trees > Advanced (topic=13, sub=62)
    add(1,13,62,"Serialize and Deserialize Binary Tree","hard","coding",
        "Design algorithm to serialize/deserialize a binary tree.",
        "BFS/DFS preorder with null markers. Serialize: preorder traversal writing values and 'null'. Deserialize: use queue, reconstruct from preorder sequence. O(n).",
        ["trees","design"],["Facebook","Amazon"])
    add(1,13,62,"Binary Tree Maximum Path Sum","hard","coding",
        "Find the maximum path sum in a binary tree (path can go through any nodes).",
        "DFS: at each node, max gain = max(0, left_gain, right_gain) + node.val. Update global max with left+right+node. Return max single-path gain. O(n).",
        ["trees","dp"],["Google","Amazon"])

    # =========================================================
    # OOPS — subject_id=2
    # =========================================================

    # Pillars > Polymorphism (topic=21, sub=91)
    add(2,21,91,"What is Polymorphism?","easy","conceptual",
        "Explain polymorphism in OOP. What are its types?",
        "Polymorphism means 'many forms'. Types: (1) Compile-time (method overloading) - same name, different params. (2) Runtime (method overriding) - subclass overrides parent. Enables writing generic code that works with different objects.",
        ["polymorphism","oops"],["TCS","Infosys"])
    add(2,21,91,"Method Overloading vs Overriding","easy","conceptual",
        "What is the difference between method overloading and method overriding?",
        "Overloading: same method name, different parameters, resolved at compile time (static polymorphism). Overriding: subclass redefines parent's method with same signature, resolved at runtime (dynamic polymorphism). Overriding requires inheritance.",
        ["polymorphism","oops"],["Amazon","Microsoft"])
    add(2,21,91,"Runtime Polymorphism Example","medium","coding",
        "Write a Python example demonstrating runtime polymorphism with animals.",
        "Define Animal base class with speak(). Dog and Cat override speak(). Call speak() via Animal reference: for animal in [Dog(), Cat()]: animal.speak(). Python uses duck typing; no explicit override keyword needed.",
        ["polymorphism","python"],["Wipro","Accenture"])
    add(2,21,91,"Duck Typing and Polymorphism","medium","conceptual",
        "How does duck typing relate to polymorphism in Python?",
        "Duck typing: 'if it walks like a duck and quacks like a duck, it's a duck'. Python doesn't check class hierarchy, only if object has required method. Enables polymorphism without inheritance. Contrast with Java's explicit interface implementation.",
        ["polymorphism","python"],["Google","Netflix"])
    add(2,21,91,"Operator Overloading","medium","coding",
        "Explain operator overloading with a Vector class example in Python.",
        "Define __add__, __mul__ etc. dunder methods. E.g., Vector(1,2) + Vector(3,4) calls __add__ and returns Vector(4,6). Allows intuitive syntax for custom objects. A form of compile-time polymorphism.",
        ["polymorphism","python"],["Amazon"])

    # Pillars > Encapsulation (topic=21, sub=88)
    add(2,21,88,"What is Encapsulation?","easy","conceptual",
        "Explain encapsulation with a real-world example.",
        "Encapsulation bundles data (attributes) and methods that operate on data into a single unit (class), and restricts direct access. Like a pill capsule—internal ingredients hidden. Use private attributes with public getters/setters. Protects data integrity.",
        ["encapsulation","oops"],["TCS","Infosys"])
    add(2,21,88,"Getter and Setter in Python","easy","coding",
        "Implement a BankAccount class with proper encapsulation using Python properties.",
        "Use @property for getter, @balance.setter for setter with validation. Private attribute _balance. Setter validates: no negative deposits. This is Pythonic encapsulation vs explicit get/set methods.",
        ["encapsulation","python"],["Amazon"])
    add(2,21,88,"Information Hiding Benefits","medium","conceptual",
        "Why is information hiding important in software design?",
        "Reduces coupling (callers don't depend on implementation details). Enables changing implementation without breaking callers. Prevents invalid state via validation in setters. Simplifies debugging (single point of data modification).",
        ["encapsulation","design"],["Google"])

    # Pillars > Abstraction (topic=21, sub=89)
    add(2,21,89,"Abstract Classes vs Interfaces","medium","conceptual",
        "What is the difference between abstract classes and interfaces? When to use each?",
        "Abstract class: can have concrete methods, constructor, state. Interface: only abstract methods (contract). Use abstract class for shared base implementation (is-a). Use interface for behavior contract across unrelated classes (can-do). Python uses ABC; no explicit interface keyword.",
        ["abstraction","oops"],["Amazon","Microsoft"])
    add(2,21,89,"Python ABC Example","medium","coding",
        "Implement an abstract Shape class and concrete Circle, Rectangle subclasses.",
        "from abc import ABC, abstractmethod. class Shape(ABC): @abstractmethod def area(self): pass. class Circle(Shape): def area(self): return pi*r². Cannot instantiate Shape directly. Forces subclasses to implement area().",
        ["abstraction","python"],["Google"])
    add(2,21,89,"Abstraction vs Encapsulation","easy","conceptual",
        "What is the difference between abstraction and encapsulation?",
        "Abstraction hides complexity (what an object does — shows interface, hides implementation). Encapsulation hides data (wraps data and methods, restricts access). Abstraction is a design principle; encapsulation is the implementation mechanism. Both reduce complexity at different levels.",
        ["abstraction","encapsulation"],["TCS","Infosys"])

    # Pillars > Inheritance (topic=21, sub=90)
    add(2,21,90,"Multiple Inheritance and MRO","hard","conceptual",
        "How does Python handle multiple inheritance? Explain MRO.",
        "Python uses C3 linearization (MRO - Method Resolution Order). super() follows MRO. Use mro() or __mro__ to see order. Diamond problem: Python only calls each parent once. Prefer composition over deep inheritance hierarchies.",
        ["inheritance","python"],["Google","Amazon"])
    add(2,21,90,"Composition vs Inheritance","medium","conceptual",
        "When should you prefer composition over inheritance?",
        "Prefer composition when: relationship is 'has-a' not 'is-a', you want more flexibility (can change at runtime), avoiding fragile base class problem, testing (easier to mock). Inheritance for: true is-a relationships, code reuse of concrete behavior.",
        ["inheritance","design"],["Netflix","Uber"])
    add(2,21,90,"Liskov Substitution Principle","medium","conceptual",
        "Explain the Liskov Substitution Principle with an example.",
        "Objects of subclass must be usable wherever parent class is expected without breaking program. Classic violation: Square extends Rectangle but setWidth changes height too. Fix: don't extend if behavior contracts differ. LSP ensures subtypes honor parent contracts.",
        ["inheritance","SOLID"],["Amazon","Microsoft"])

    # Design Principles > SOLID (topic=22, sub=92)
    add(2,22,92,"Single Responsibility Principle","medium","conceptual",
        "Explain SRP with a code example. What problem does it solve?",
        "A class should have only one reason to change. Bad: UserManager handles auth + email + DB. Good: split into AuthService, EmailService, UserRepository. Reduces coupling, easier testing, changes to email don't affect auth logic.",
        ["SOLID","SRP"],["Amazon","Google"])
    add(2,22,92,"Open Closed Principle","medium","conceptual",
        "Explain OCP. How does it relate to strategy pattern?",
        "Open for extension, closed for modification. Add new features by extending, not changing existing code. Example: Discount calculator — instead of if/elif for each type, create DiscountStrategy interface with subclasses. New discount type = new class, no existing code change.",
        ["SOLID","OCP"],["Amazon"])
    add(2,22,92,"Dependency Inversion Principle","hard","conceptual",
        "Explain DIP and how it enables dependency injection.",
        "High-level modules shouldn't depend on low-level modules; both should depend on abstractions. Instead of DatabaseService directly creating MySQLDB, inject it via constructor taking IDatabase interface. Enables swapping implementations (MySQL→Postgres), easier testing with mocks.",
        ["SOLID","DIP"],["Google","Microsoft"])
    add(2,22,92,"Interface Segregation Principle","medium","conceptual",
        "Explain ISP with an example of a fat interface.",
        "Clients shouldn't be forced to depend on interfaces they don't use. Fat interface: Worker has work() + eat() + sleep(). Robot must implement eat() and sleep() even though irrelevant. Fix: split into Workable, Feedable, Sleepable interfaces.",
        ["SOLID","ISP"],["Amazon"])

    # Design Patterns > Singleton (topic=23, sub=93)
    add(2,23,93,"Thread-Safe Singleton in Python","hard","coding",
        "Implement a thread-safe Singleton pattern in Python.",
        "Use threading.Lock() in __new__ method. Double-checked locking: check instance, lock, check again, create if needed. Alternatively use module-level instance (Python modules are imported once). Or use metaclass approach.",
        ["singleton","threading"],["Amazon","Google"])
    add(2,23,93,"When to Avoid Singleton","medium","conceptual",
        "What are the drawbacks of the Singleton pattern?",
        "Global state makes testing hard (can't reset between tests). Tight coupling (hidden dependency). Violates SRP (manages own lifecycle). Concurrency issues if not thread-safe. Alternative: dependency injection with single instance at composition root.",
        ["singleton","design"],["Netflix"])

    # Design Patterns > Factory (topic=23, sub=94)
    add(2,23,94,"Factory Method Pattern","medium","conceptual",
        "Explain the Factory Method pattern with a real-world example.",
        "Defines interface for creating object but lets subclass decide which class to instantiate. Example: LoggerFactory.create('file') returns FileLogger, create('db') returns DBLogger. Caller doesn't know concrete class. Follows OCP — add new types by adding new factory branch.",
        ["factory","design_patterns"],["Amazon","Microsoft"])
    add(2,23,94,"Abstract Factory vs Factory Method","hard","conceptual",
        "What is the difference between Abstract Factory and Factory Method patterns?",
        "Factory Method: single method that creates one product type. Abstract Factory: creates families of related objects. Example: UIFactory with createButton() and createCheckbox(). WindowsFactory returns WindowsButton+WindowsCheckbox; MacFactory returns Mac variants. Abstract Factory uses Factory Methods internally.",
        ["factory","design_patterns"],["Google"])
    add(2,23,94,"Python Factory Implementation","medium","coding",
        "Implement a Shape factory in Python that creates Circle, Square, Triangle objects.",
        "def create_shape(shape_type, **kwargs): shapes = {'circle': Circle, 'square': Square, 'triangle': Triangle}. return shapes[shape_type](**kwargs). Alternatively use class method or dict registry. Decouples object creation from usage.",
        ["factory","python"],["Amazon"])
    add(2,23,94,"Builder Pattern vs Factory","medium","conceptual",
        "When would you use Builder pattern instead of Factory?",
        "Factory for simple creation with variants. Builder for complex objects with many optional parameters (telescoping constructor problem). Example: HTTPRequest.Builder().url(...).method('GET').header(...).timeout(30).build(). Each step is optional, order doesn't matter. Prevents invalid partial objects.",
        ["factory","builder","design_patterns"],["Uber","Airbnb"])
    add(2,23,94,"Factory Pattern Use Case","easy","conceptual",
        "Give a real production use case where factory pattern is essential.",
        "Database connection factory: create connection based on config (MySQL, PostgreSQL, SQLite). Plugin systems. Notification factory (Email, SMS, Push). Payment processor factory (Stripe, PayPal, Razorpay). Game character factory. All cases where type is determined at runtime.",
        ["factory","design_patterns"],["PayPal","Stripe"])

    # Design Patterns > Observer (topic=23, sub=95)
    add(2,23,95,"Observer Pattern Explained","medium","conceptual",
        "Explain the Observer pattern. What problem does it solve?",
        "Defines one-to-many dependency: when subject changes state, all observers are notified automatically. Solves tight coupling between event source and handlers. Examples: event listeners in UI, pub-sub systems, MVC (view observes model). Follows Open-Closed: add observers without changing subject.",
        ["observer","design_patterns"],["Amazon","Google"])
    add(2,23,95,"Python Observer Implementation","medium","coding",
        "Implement an Observer pattern for a stock price notifier in Python.",
        "Subject: StockMarket with observers list, register(), deregister(), notify(). Observer: interface with update(price). Concrete: EmailAlert, SMSAlert implement update(). market.price = 150 triggers notify() which calls all observers. Pure Python without external libraries.",
        ["observer","python"],["Goldman Sachs"])
    add(2,23,95,"Event Emitter as Observer Pattern","medium","conceptual",
        "How does Node.js EventEmitter implement the Observer pattern?",
        "EventEmitter IS the Observer pattern: emitter.on('event', callback) = register observer. emitter.emit('event', data) = notify all observers. removeListener() = deregister. Multiple listeners for same event. Python equivalent: signals in Django, events in asyncio.",
        ["observer","events"],["Netflix","Uber"])
    add(2,23,95,"Pub-Sub vs Observer","hard","conceptual",
        "What is the difference between Observer pattern and Pub-Sub pattern?",
        "Observer: direct coupling — observers know subject, subject holds observer references. Synchronous. Pub-Sub: decoupled via message broker — publishers/subscribers don't know each other. Asynchronous. Examples: Observer=Django signals, Pub-Sub=Kafka/RabbitMQ. Pub-Sub scales better for distributed systems.",
        ["observer","pubsub","distributed"],["Amazon","Kafka"])
    add(2,23,95,"Reactive Programming and Observers","hard","conceptual",
        "How does reactive programming (RxPY/RxJS) extend the Observer pattern?",
        "Rx extends Observer with: streams of events (not single), operators (map, filter, merge), backpressure, error handling, completion signals. Observable = enhanced Subject. Observer gets onNext, onError, onComplete. Enables composable async event pipelines. Used in Angular, Android.",
        ["observer","reactive"],["Google","Netflix"])

    # =========================================================
    # SYSTEM DESIGN — subject_id=3
    # =========================================================

    # Scalability > Basics (topic=24, sub=96)
    add(3,24,96,"Horizontal vs Vertical Scaling","easy","conceptual",
        "What is the difference between horizontal and vertical scaling? When to use each?",
        "Vertical (scale up): add CPU/RAM to existing server. Simple but has limits, single point of failure, expensive. Horizontal (scale out): add more servers. Requires load balancer, stateless services, more complex but unlimited scale, no SPOF. Modern systems prefer horizontal.",
        ["scalability","system_design"],["Amazon","Google"])
    add(3,24,96,"Load Balancing Algorithms","medium","conceptual",
        "Explain different load balancing algorithms and when to use each.",
        "Round Robin: equal distribution, simple. Weighted RR: servers with different capacities. Least Connections: route to server with fewest active connections. IP Hash: sticky sessions (same client to same server). Consistent Hashing: minimal redistribution on server add/remove. Health checks integrated in all.",
        ["load_balancing","scalability"],["Amazon","Cloudflare"])
    add(3,24,96,"CAP Theorem in System Design","hard","conceptual",
        "Explain CAP theorem and how it affects system design decisions.",
        "CAP: Consistency (all nodes see same data), Availability (system responds), Partition Tolerance (continues despite network failure). Can only guarantee 2 of 3. P always needed in distributed systems. CA=RDBMS. CP=MongoDB, HBase (sacrifice availability). AP=Cassandra, DynamoDB (sacrifice consistency). Choose based on business requirements.",
        ["CAP","consistency","distributed"],["Amazon","Google"])
    add(3,24,96,"Microservices vs Monolith","medium","conceptual",
        "Compare microservices and monolithic architectures. When to choose each?",
        "Monolith: simple, single codebase, easy debugging, good for small teams. Microservices: independent deployment, tech heterogeneity, fault isolation, scales per service. Choose monolith initially. Migrate to microservices when: team grows, need independent scaling, different tech requirements per service.",
        ["microservices","architecture"],["Netflix","Uber"])
    add(3,24,96,"Database Sharding Strategies","hard","conceptual",
        "Explain different database sharding strategies and their trade-offs.",
        "Range-based: shard by ID ranges. Simple but hotspots. Hash-based: hash(key) % shards. Even distribution but resharding painful. Directory-based: lookup service maps key to shard. Flexible but lookup is bottleneck. Consistent hashing: minimal resharding. Geographic: shard by location for latency.",
        ["sharding","database","scalability"],["Amazon","Facebook"])

    # Caching > Basics (topic=25, sub=97)
    add(3,25,97,"Cache Invalidation Strategies","medium","conceptual",
        "Explain different cache invalidation strategies.",
        "Write-through: write to cache and DB simultaneously. Consistent, but higher write latency. Write-back: write to cache, async to DB. Fast writes, risk of loss. Write-around: write directly to DB, bypass cache. Good for write-once read-rarely data. Cache-aside: app manages cache explicitly. Most flexible.",
        ["caching","redis"],["Amazon","Facebook"])
    add(3,25,97,"CDN Architecture","medium","conceptual",
        "How does a CDN work? When would you use one?",
        "CDN: distributed servers (PoPs) geographically close to users. Cache static content (images, JS, video). User request → nearest PoP. Cache miss → origin server. TTL controls freshness. Use for: static assets, video streaming, global users, reducing origin load. Examples: CloudFront, Akamai, Fastly.",
        ["CDN","caching"],["Netflix","Cloudflare"])
    add(3,25,97,"Redis vs Memcached","easy","conceptual",
        "When would you choose Redis over Memcached?",
        "Redis: supports data structures (lists, sets, sorted sets), persistence, pub-sub, Lua scripting, clustering, atomic operations. Memcached: simple key-value, multi-threaded (better for pure caching at scale), less memory overhead. Choose Redis for: session storage, leaderboards, pub-sub, persistence. Memcached for: simple pure caching.",
        ["redis","caching"],["Amazon","Uber"])
    add(3,25,97,"Cache Stampede Prevention","hard","conceptual",
        "What is a cache stampede and how do you prevent it?",
        "Cache stampede (thundering herd): many requests hit DB simultaneously when cache expires. Prevention: (1) Mutex locking: only one request rebuilds, others wait. (2) Probabilistic early expiration: pre-expire before actual TTL. (3) Stale-while-revalidate: serve stale while rebuilding. (4) Background refresh before expiry.",
        ["caching","performance"],["Facebook","Netflix"])

    # URL Shortener > Design (topic=26, sub=98)
    add(3,26,98,"URL Shortener System Design","hard","system_design",
        "Design a URL shortener like bit.ly. Handle 100M URLs, 10B redirects/day.",
        "API: POST /shorten, GET /{code}→302 redirect. Short code: Base62(MD5 hash) or auto-increment ID. DB: SQL for URL mappings. Cache: Redis for hot URLs (90% traffic from 20% URLs). Scale: read-heavy → many read replicas. CDN for global low latency. Analytics: Kafka→ClickHouse. Handle custom aliases, expiry.",
        ["url_shortener","system_design"],["Amazon","Google"])
    add(3,26,98,"Collision Handling in URL Shortener","medium","conceptual",
        "How do you handle hash collisions in a URL shortener?",
        "MD5 of URL → first 6 chars of Base62. Collision: same short code for different URLs. Solutions: (1) Check DB, append counter if collision, retry. (2) Use Bloom filter to quickly check existence. (3) Pre-generate short codes (offline generation). (4) Use UUID/snowflake ID → Base62 (no collision by design).",
        ["url_shortener","hashing"],["Amazon"])
    add(3,26,98,"Analytics for URL Shortener","medium","conceptual",
        "How would you add click analytics to a URL shortener at scale?",
        "Don't write to DB on every redirect (too slow). Write to Kafka on each click. Kafka consumers aggregate and batch-write to analytics DB (ClickHouse/BigQuery). For real-time: Storm/Flink processing. Show: total clicks, per-country, per-device, per-day. Cache popular URL stats in Redis.",
        ["url_shortener","analytics","kafka"],["Bitly"])

    # Rate Limiter > Design (topic=27, sub=99)
    add(3,27,99,"Rate Limiter Algorithms","hard","conceptual",
        "Explain different rate limiting algorithms. Which does Stripe/Nginx use?",
        "Token Bucket: tokens added at fixed rate, request consumes token. Allows bursts. Leaky Bucket: fixed output rate, queue excess. Smooth traffic. Fixed Window: count per time window. Boundary issue. Sliding Window Log: track exact timestamps. Accurate but memory-heavy. Sliding Window Counter: compromise. Redis atomic ops for distributed.",
        ["rate_limiter","algorithms"],["Stripe","Cloudflare"])
    add(3,27,99,"Distributed Rate Limiting","hard","conceptual",
        "How do you implement rate limiting across multiple servers?",
        "Centralized: Redis as shared counter. Atomic INCR + EXPIRE. Pros: accurate. Cons: Redis latency, SPOF. Distributed: each server tracks locally, sync periodically (eventual consistency, some burst allowed). Consistent hashing: route same user to same server. Sticky sessions. Lua scripts for atomicity in Redis.",
        ["rate_limiter","distributed","redis"],["Stripe","Uber"])
    add(3,27,99,"Rate Limiter API Design","medium","conceptual",
        "Design the API response for a rate limiter. What headers should you return?",
        "Standard headers: X-RateLimit-Limit (max requests), X-RateLimit-Remaining (left), X-RateLimit-Reset (epoch when limit resets). On exceed: HTTP 429 Too Many Requests + Retry-After header. For APIs: per-user, per-endpoint, per-IP limits. Different tiers (free vs paid). Circuit breaker integration.",
        ["rate_limiter","api_design"],["Stripe","GitHub"])
    add(3,27,99,"Rate Limiter Storage Design","medium","conceptual",
        "What storage solution would you choose for a rate limiter and why?",
        "Redis: best choice. In-memory O(1), supports atomic operations (INCR, EXPIRE), TTL built-in, Lua scripts for atomicity, cluster mode for HA. Alternative: Memcached (no persistence). Avoid SQL DB (too slow for every request). Local in-memory for single-server. Redis Sentinel for HA.",
        ["rate_limiter","redis"],["Cloudflare"])

    # Distributed Systems > Expert (topic=28, sub=100)
    add(3,28,100,"Consistent Hashing","hard","conceptual",
        "Explain consistent hashing. Why is it used in distributed systems?",
        "Consistent hashing: map both nodes and keys to a ring. Key assigned to nearest clockwise node. Adding/removing node: only K/N keys reassigned (vs all keys in modulo hashing). Virtual nodes: each physical node has multiple ring positions for even distribution. Used in: DynamoDB, Cassandra, Memcached.",
        ["consistent_hashing","distributed"],["Amazon","Facebook"])
    add(3,28,100,"Two-Phase Commit vs Saga Pattern","hard","conceptual",
        "Compare 2PC and Saga for distributed transactions.",
        "2PC: coordinator + participants. Phase1: prepare (can you commit?). Phase2: commit/rollback. Blocking: coordinator failure leaves participants in uncertain state. Saga: sequence of local transactions with compensating transactions for rollback. Choreography (events) or orchestration (coordinator). Better for microservices—no distributed lock.",
        ["distributed","transactions","saga"],["Uber","Amazon"])
    add(3,28,100,"Design a Distributed Message Queue","hard","system_design",
        "Design a message queue like Kafka. Focus on durability and throughput.",
        "Topics partitioned across brokers. Producers write to leader partition. Replication factor=3 for durability. Consumers in consumer groups—each partition consumed by one consumer. Offsets stored in ZooKeeper/internal topic. Page cache for fast writes. Sequential disk I/O. Zero-copy via sendfile(). 1M+ msgs/sec per broker.",
        ["kafka","distributed","message_queue"],["LinkedIn","Confluent"])
    add(3,28,100,"Leader Election in Distributed Systems","hard","conceptual",
        "How does leader election work in distributed systems?",
        "Problem: need single leader for coordination. Algorithms: Bully (highest ID wins, re-elect on failure), Ring (pass token around ring). In practice: ZooKeeper (ephemeral znodes—first to create wins), etcd (Raft consensus), Redis RedLock. Raft/Paxos: quorum-based consensus. Used in: Kafka (ZK→KRaft), Kubernetes (etcd), MongoDB replica sets.",
        ["distributed","leader_election","consensus"],["Google","Amazon"])
    add(3,28,100,"Event Sourcing and CQRS","hard","conceptual",
        "Explain Event Sourcing and CQRS. When would you use them together?",
        "Event Sourcing: store sequence of events, not current state. Rebuild state by replaying events. Full audit log. CQRS: separate read and write models. Write model handles commands, read model optimized for queries. Together: events published to read side (projections). Good for: audit trails, temporal queries, high read/write ratio. Complexity cost: eventual consistency, event schema evolution.",
        ["event_sourcing","CQRS","distributed"],["Netflix","Stripe"])

    # =========================================================
    # DBMS — subject_id=4
    # =========================================================

    # Fundamentals (topic=29, sub=101)
    add(4,29,101,"DBMS vs File System","easy","conceptual",
        "Why use a DBMS over a file system? List key advantages.",
        "DBMS provides: (1) Data independence (change storage without changing app). (2) ACID transactions. (3) Concurrent access control. (4) Query optimization. (5) Security (user permissions). (6) Backup/recovery. (7) Integrity constraints. File system: no query language, no transactions, manual concurrency control.",
        ["dbms","fundamentals"],["TCS","Infosys"])
    add(4,29,101,"Primary Key vs Foreign Key vs Unique Key","easy","conceptual",
        "Explain the difference between Primary, Foreign, and Unique keys.",
        "Primary Key: uniquely identifies each row, NOT NULL, one per table, clustered index by default. Foreign Key: references primary key of another table, enforces referential integrity, can be NULL. Unique Key: enforces uniqueness, can have NULL (multiple NULLs allowed in some DBs), multiple per table.",
        ["dbms","keys"],["Amazon","Microsoft"])
    add(4,29,101,"ER Diagram to Relational Schema","medium","conceptual",
        "How do you convert an ER diagram to a relational schema?",
        "Rules: (1) Entity → table, attributes → columns. (2) 1:1 relationship → FK in either table. (3) 1:N → FK in N-side table. (4) M:N → junction table with both PKs as FKs. (5) Weak entity → include owner's PK. (6) Multivalued attribute → separate table. (7) Subtype/supertype → table per type or combined.",
        ["dbms","ER","schema"],["Microsoft"])
    add(4,29,101,"OLTP vs OLAP","medium","conceptual",
        "Compare OLTP and OLAP databases. Give examples of each.",
        "OLTP: operational, high transaction volume, simple queries, row-oriented storage, normalized schema. Examples: MySQL, PostgreSQL. OLAP: analytical, complex aggregations, large data scans, column-oriented (fast aggregation), denormalized star/snowflake schema. Examples: BigQuery, Redshift, ClickHouse. Modern: HTAP (MySQL HeatWave, TiDB).",
        ["dbms","OLTP","OLAP"],["Amazon","Google"])

    # Transactions > ACID (topic=30, sub=102)
    add(4,30,102,"Isolation Levels Explained","hard","conceptual",
        "Explain the 4 SQL isolation levels and what anomalies each prevents.",
        "READ UNCOMMITTED: dirty reads possible. READ COMMITTED (PG default): prevents dirty reads. REPEATABLE READ (MySQL default): prevents non-repeatable reads. SERIALIZABLE: prevents phantom reads, full isolation. Trade-off: higher isolation = lower concurrency. Anomalies: dirty read (reading uncommitted), non-repeatable (same row changes), phantom (new rows appear in range query).",
        ["ACID","isolation","transactions"],["Amazon","Microsoft"])
    add(4,30,102,"Distributed Transactions","hard","conceptual",
        "How do databases handle distributed transactions? What is XA protocol?",
        "XA: standard two-phase commit for distributed transactions. Transaction coordinator manages multiple resource managers (DBs). Phase1: prepare (all must agree). Phase2: commit or rollback. Issues: blocking if coordinator fails, slow. Modern alternatives: Saga pattern, TCC (Try-Confirm-Cancel), eventual consistency. XA supported by: MySQL, PostgreSQL, Oracle.",
        ["ACID","distributed","transactions"],["Oracle","Amazon"])
    add(4,30,102,"MVCC - Multi-Version Concurrency Control","hard","conceptual",
        "Explain MVCC. How does PostgreSQL use it?",
        "MVCC maintains multiple versions of data to allow concurrent reads and writes without locking. Readers don't block writers, writers don't block readers. Each row has xmin (created by), xmax (deleted by). Transaction sees snapshot of DB at its start. PostgreSQL uses MVCC; dead tuples need VACUUM. MySQL InnoDB uses similar approach.",
        ["ACID","MVCC","postgresql"],["PostgreSQL","Oracle"])
    add(4,30,102,"Transaction Savepoints","medium","conceptual",
        "What are savepoints in SQL transactions? How do they work?",
        "Savepoints allow partial rollback within a transaction. SAVEPOINT sp1; ... ROLLBACK TO SAVEPOINT sp1; rolls back to that point without aborting whole transaction. Useful for complex operations where you want to retry part of it. Nested transactions in effect. Supported by PostgreSQL, Oracle. MySQL: partial support.",
        ["transactions","SQL"],["Oracle"])

    # Normalization (topic=31, sub=103)
    add(4,31,103,"Denormalization and When to Use It","medium","conceptual",
        "What is denormalization? When would you choose it over normalization?",
        "Denormalization: intentionally add redundancy to improve read performance. Store computed/duplicate data. Trade-off: faster reads but complex writes, more storage. Use when: read-heavy workload, complex joins are bottleneck, OLAP analytics, caching frequently joined data. Examples: storing user's name in orders table instead of joining.",
        ["normalization","performance"],["Amazon","Facebook"])
    add(4,31,103,"1NF 2NF 3NF with Examples","medium","conceptual",
        "Explain 1NF, 2NF, and 3NF with concrete examples.",
        "1NF: atomic values, no repeating groups. 2NF: 1NF + no partial dependency (non-key attribute fully dependent on entire PK). 3NF: 2NF + no transitive dependency (A→B→C: B and C must both depend directly on PK). Example: Order(OrderID, ProductID, ProductName, CustomerCity). ProductName depends on ProductID (partial) → violates 2NF. CustomerCity depends on CustomerID (transitive) → violates 3NF.",
        ["normalization","schema"],["TCS","Microsoft"])
    add(4,31,103,"BCNF - Boyce-Codd Normal Form","hard","conceptual",
        "What is BCNF and how does it differ from 3NF?",
        "BCNF: stricter than 3NF. Every functional dependency X→Y must have X as superkey. 3NF allows non-trivial FDs where Y is prime attribute. BCNF eliminates all FD anomalies. Sometimes BCNF decomposition loses dependency preservation. In practice 3NF is often sufficient. 4NF handles multi-valued dependencies.",
        ["normalization","BCNF"],["Microsoft","Oracle"])

    # SQL > Basics (topic=32, sub=104)
    add(4,32,104,"Window Functions in SQL","hard","coding",
        "Write SQL to find the second highest salary in each department using window functions.",
        "SELECT dept, name, salary FROM (SELECT dept, name, salary, DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) as rnk FROM employees) t WHERE rnk = 2. Window functions: ROW_NUMBER (unique), RANK (gaps), DENSE_RANK (no gaps). Also: LAG, LEAD, FIRST_VALUE, LAST_VALUE.",
        ["SQL","window_functions"],["Amazon","Google"])
    add(4,32,104,"SQL HAVING vs WHERE","easy","conceptual",
        "What is the difference between WHERE and HAVING clauses?",
        "WHERE filters rows before grouping (cannot use aggregate functions). HAVING filters groups after GROUP BY (can use aggregates). Execution order: FROM→WHERE→GROUP BY→HAVING→SELECT→ORDER BY→LIMIT. Example: WHERE salary > 50000 (row level). HAVING AVG(salary) > 50000 (group level).",
        ["SQL","fundamentals"],["TCS","Wipro"])
    add(4,32,104,"SQL Subqueries vs JOINs","medium","conceptual",
        "When should you use a subquery versus a JOIN?",
        "JOIN: better for fetching columns from multiple tables, usually faster (optimizer can use indexes). Subquery: better for filter conditions (WHERE id IN (subquery)), correlated subqueries for row-by-row logic. EXISTS vs IN: EXISTS short-circuits (faster for large datasets). Modern optimizers often convert subqueries to JOINs.",
        ["SQL","performance"],["Amazon","Microsoft"])

    # SQL > Joins (topic=32, sub=105)
    add(4,32,105,"Explain SQL Join Types","easy","conceptual",
        "Explain INNER, LEFT, RIGHT, FULL OUTER, and CROSS joins with examples.",
        "INNER JOIN: only matching rows from both tables. LEFT JOIN: all rows from left + matching from right (NULL for no match). RIGHT JOIN: reverse of LEFT. FULL OUTER JOIN: all rows from both, NULL where no match. CROSS JOIN: cartesian product (every combo). SELF JOIN: table joined with itself (org hierarchy). In practice: LEFT JOIN most common, CROSS JOIN for combinations.",
        ["SQL","joins"],["Amazon","TCS"])
    add(4,32,105,"Find Employees Without Managers (LEFT JOIN)","easy","coding",
        "Write SQL to find all employees who have no manager using a LEFT JOIN.",
        "SELECT e.name FROM employees e LEFT JOIN employees m ON e.manager_id = m.id WHERE m.id IS NULL. Or: WHERE manager_id IS NULL (simpler). Self-join on same table to find unmatched rows. LEFT JOIN + IS NULL = anti-join pattern (equivalent to NOT IN / NOT EXISTS).",
        ["SQL","joins","self_join"],["Amazon","Microsoft"])
    add(4,32,105,"SQL Anti-Join Pattern","medium","coding",
        "Find all customers who have never placed an order using three different SQL methods.",
        "Method1 (LEFT JOIN+NULL): SELECT c.* FROM customers c LEFT JOIN orders o ON c.id=o.customer_id WHERE o.id IS NULL. Method2 (NOT IN): WHERE id NOT IN (SELECT customer_id FROM orders). Method3 (NOT EXISTS): WHERE NOT EXISTS (SELECT 1 FROM orders WHERE customer_id=c.id). NOT EXISTS usually fastest.",
        ["SQL","joins","anti_join"],["Amazon","Google"])
    add(4,32,105,"Complex JOIN with Aggregation","hard","coding",
        "Write SQL to find the department with the highest average salary and return top 3 employees from it.",
        "WITH dept_avg AS (SELECT dept_id, AVG(salary) avg_sal FROM employees GROUP BY dept_id ORDER BY avg_sal DESC LIMIT 1), top_emp AS (SELECT e.*, RANK() OVER (ORDER BY salary DESC) rnk FROM employees WHERE dept_id = (SELECT dept_id FROM dept_avg)) SELECT * FROM top_emp WHERE rnk <= 3. CTEs + window functions.",
        ["SQL","joins","CTE","window_functions"],["Google","Amazon"])
    add(4,32,105,"JOIN Performance Optimization","medium","conceptual",
        "How do you optimize slow SQL JOIN queries?",
        "Strategies: (1) Index join columns (FK and PK). (2) Filter early with WHERE before JOIN. (3) Avoid SELECT * — fetch only needed columns. (4) Use EXPLAIN/EXPLAIN ANALYZE to find sequential scans. (5) Consider covering indexes. (6) Materialized views for complex joins. (7) Partition large tables. (8) Denormalize if joins are constant bottleneck.",
        ["SQL","joins","performance"],["Amazon","PostgreSQL"])

    # Indexing (topic=33, sub=106)
    add(4,33,106,"Clustered vs Non-Clustered Index","medium","conceptual",
        "What is the difference between clustered and non-clustered indexes?",
        "Clustered: determines physical row storage order. One per table (usually PK). B-Tree where leaf nodes = actual data. Non-clustered: separate structure with pointer to row. Multiple per table. Leaf nodes store key + row pointer (bookmark). Clustered faster for range queries. Non-clustered adds write overhead. In PostgreSQL, all indexes are non-clustered (heap-based).",
        ["indexing","database"],["Amazon","Microsoft"])
    add(4,33,106,"Composite Index and Index Selectivity","hard","conceptual",
        "Explain composite indexes and the concept of index selectivity.",
        "Composite index: index on multiple columns. (a, b, c) can be used for queries on (a), (a,b), (a,b,c) — left prefix rule. Selectivity: ratio of distinct values to total rows. High selectivity = better index candidate (gender column = low selectivity, bad index). Covering index: all query columns in index, avoids table lookup.",
        ["indexing","composite_index"],["Google","Amazon"])
    add(4,33,106,"When NOT to Use Indexes","medium","conceptual",
        "In what scenarios should you avoid creating an index?",
        "Avoid indexes on: (1) Small tables (full scan faster). (2) Low cardinality columns (boolean, gender). (3) Frequently updated columns (write overhead). (4) Columns rarely used in WHERE/JOIN. Too many indexes: slow INSERT/UPDATE/DELETE, more storage, optimizer confusion. Max ~5-10 indexes per table. DROP unused indexes.",
        ["indexing","performance"],["Amazon"])
    add(4,33,106,"Database Explain Plan","medium","conceptual",
        "How do you read a PostgreSQL EXPLAIN ANALYZE output?",
        "EXPLAIN ANALYZE shows: execution plan + actual times. Key nodes: Seq Scan (slow, no index), Index Scan, Index Only Scan (fastest). Nested Loop Join, Hash Join (for larger sets), Merge Join. Look for: high actual vs estimated rows (stale statistics→ANALYZE), sequential scans on large tables, expensive sort operations. Use for tuning.",
        ["indexing","postgresql","performance"],["PostgreSQL"])

    # Concurrency (topic=34, sub=107)
    add(4,34,107,"Optimistic vs Pessimistic Locking","medium","conceptual",
        "Explain optimistic and pessimistic locking. When to use each?",
        "Pessimistic: lock before read (SELECT FOR UPDATE). Assumes conflicts frequent. Prevents concurrent access. Deadlock risk. Good for high-contention. Optimistic: no lock on read, version check on write (UPDATE ... WHERE version=expected). Retry on conflict. Better for low-contention. Uses version column or timestamp. ORM support: Hibernate @Version.",
        ["concurrency","locking"],["Amazon","Oracle"])
    add(4,34,107,"Deadlock Detection and Prevention","medium","conceptual",
        "How do databases detect and prevent deadlocks?",
        "Detection: wait-for graph. Cycle = deadlock. DB kills one transaction (victim). Prevention: (1) Order resource acquisition consistently. (2) Lock timeout. (3) Try NOWAIT or SKIP LOCKED. (4) Acquire all locks at once. PostgreSQL: automatic deadlock detection, random victim. Best practice: keep transactions short, same lock ordering.",
        ["concurrency","deadlock"],["PostgreSQL","Oracle"])

    # Distributed DB (topic=35, sub=108)
    add(4,35,108,"Eventual Consistency Explained","medium","conceptual",
        "What is eventual consistency? Give a real-world example.",
        "Eventual consistency: in absence of updates, all replicas converge to same value eventually. No guarantee on when. Example: DNS propagation, Amazon shopping cart (dynamo). Read your own writes: not guaranteed. Monotonic read: might see older version. CRDT: conflict-free replicated data types for automatic merge. Acceptable for: social likes, view counts, shopping carts.",
        ["CAP","consistency","distributed"],["Amazon","Cassandra"])
    add(4,35,108,"Read Replicas vs Master-Slave","medium","conceptual",
        "Explain read replica architecture. What are its limitations?",
        "Master receives all writes, replicas serve reads. Replication lag: replicas may lag behind master (async replication). Read your own writes issue. Solution: read from master for critical data, replicas for analytics. Semi-sync replication: wait for at least one replica. Strong consistency requires all reads from master. Use case: read-heavy reporting queries.",
        ["distributed","replication"],["MySQL","PostgreSQL"])
    add(4,35,108,"NewSQL Databases","hard","conceptual",
        "What are NewSQL databases? How do they differ from NoSQL?",
        "NewSQL: ACID + horizontal scalability (best of SQL+NoSQL). Examples: Google Spanner, CockroachDB, TiDB, YugabyteDB. Techniques: Paxos/Raft consensus, distributed transactions, sharding transparent to application. NoSQL: scale by sacrificing ACID. NewSQL: scale + keep ACID. Spanner uses atomic clocks for global consistency. Good for: financial systems needing both scale and consistency.",
        ["distributed","NewSQL"],["Google","CockroachDB"])

    # =========================================================
    # OS & Networking — subject_id=5
    # =========================================================

    # OS Basics (topic=36, sub=109)
    add(5,36,109,"Process vs Thread","easy","conceptual",
        "What is the difference between a process and a thread?",
        "Process: independent execution unit with own memory space, file handles, address space. Heavyweight. Isolation via OS. Thread: execution unit within process, shares memory, stack is private. Lightweight, faster context switch. Communication: IPC for processes (pipes, sockets), shared memory for threads. Python GIL limits thread parallelism for CPU-bound tasks.",
        ["process","thread","os"],["Amazon","Microsoft"])
    add(5,36,109,"Context Switching","medium","conceptual",
        "What is context switching? What information is saved and restored?",
        "Context switch: OS saves current process state and loads another. Saved: PC (program counter), registers, stack pointer, memory maps, file handles (PCB — Process Control Block). Cost: direct (saving/restoring registers) + indirect (cache/TLB flush). Reduce: use threads (lighter), async I/O, green threads, fibers. Linux: few microseconds per switch.",
        ["context_switch","os"],["Google","Amazon"])
    add(5,36,109,"Inter-Process Communication","medium","conceptual",
        "What are the different IPC mechanisms? When would you use each?",
        "IPC mechanisms: (1) Pipes: unidirectional, parent-child. (2) Named Pipes (FIFOs): between any processes. (3) Shared Memory: fastest, need synchronization. (4) Message Queues: kernel-buffered, async. (5) Sockets: network or local (Unix sockets). (6) Signals: async notification. (7) Semaphores: synchronization. Use shared memory for performance, sockets for networked services.",
        ["IPC","os","process"],["Linux","Amazon"])
    add(5,36,109,"User Space vs Kernel Space","medium","conceptual",
        "Explain the difference between user space and kernel space.",
        "OS memory divided into kernel space (OS code, device drivers, kernel data) and user space (user applications). User processes can't directly access kernel memory. System calls: user→kernel via trap (INT 0x80/syscall instruction). Context switch to kernel mode, execute syscall, return to user mode. Protection ring 0 (kernel), ring 3 (user). Prevents crashes/malware from corrupting kernel.",
        ["os","kernel"],["Linux","Google"])

    # Scheduling (topic=37, sub=110)
    add(5,37,110,"CPU Scheduling Algorithms","medium","conceptual",
        "Compare FCFS, SJF, Round Robin, and Priority scheduling algorithms.",
        "FCFS: simple, convoy effect (short jobs wait behind long). SJF: optimal avg wait time, needs burst time prediction, starvation possible. Round Robin: time quantum, good response time, higher overhead. Priority: starvation (aging fixes it). MLFQ: multi-level feedback queue, adapts based on behavior. Linux uses CFS (Completely Fair Scheduler) with red-black tree.",
        ["scheduling","os"],["OS","Amazon"])
    add(5,37,110,"Starvation and Aging","easy","conceptual",
        "What is starvation in scheduling? How does aging solve it?",
        "Starvation: low-priority process waits indefinitely because higher priority ones keep arriving. Aging: gradually increase priority of waiting processes. After T time units, priority increases. Eventually process gets CPU. Round Robin avoids starvation by design. Priority inversion: high priority task blocked by low priority task holding needed resource. Solution: priority inheritance protocol.",
        ["scheduling","starvation"],["OS"])
    add(5,37,110,"Real-Time Scheduling","hard","conceptual",
        "What is real-time scheduling? Explain EDF and Rate Monotonic algorithms.",
        "Real-time: tasks have deadlines. Hard RT: missing deadline is catastrophic. Soft RT: graceful degradation. Rate Monotonic: fixed priority based on period (shorter period = higher priority). Preemptive. Utilization bound: sum(Ci/Ti) ≤ 0.693. EDF: dynamic priority, always schedule earliest deadline. Optimal but higher overhead. Used in: automotive, avionics, medical devices.",
        ["scheduling","real_time"],["OS","Embedded"])

    # Memory Management (topic=38, sub=111)
    add(5,38,111,"Virtual Memory and Page Tables","medium","conceptual",
        "How does virtual memory work? What is the role of page tables?",
        "Virtual memory: each process sees own address space (0 to 2^64). Page table maps virtual page → physical frame. TLB caches recent translations. Page fault: page not in RAM, OS loads from disk (swap). Multi-level page tables save space. Benefits: isolation between processes, run programs larger than RAM, easy memory allocation.",
        ["memory","paging","os"],["OS","Google"])
    add(5,38,111,"Memory Allocation: Malloc Internals","hard","conceptual",
        "How does malloc work internally? What is heap fragmentation?",
        "malloc: requests memory from OS (sbrk/mmap). Maintains free list of blocks. Best fit, first fit, buddy system. External fragmentation: free blocks too small to satisfy large request. Internal: allocated block larger than requested. Solutions: memory pools, slab allocator (Linux kernel), jemalloc/tcmalloc for better performance. free() returns to free list.",
        ["memory","malloc","os"],["Linux","Google"])
    add(5,38,111,"Thrashing in Operating Systems","medium","conceptual",
        "What is thrashing? How does the OS prevent it?",
        "Thrashing: processes spend more time swapping pages than executing. Too many processes, not enough RAM. Each page fault evicts another needed page. Prevention: (1) Working set model: keep process's working set in memory. (2) Page fault frequency: if too high, reduce multiprogramming. (3) Add RAM. (4) Swap space tuning. Linux: kswapd background process.",
        ["memory","thrashing","os"],["OS"])

    # Deadlock (topic=39, sub=112)
    add(5,39,112,"Deadlock Conditions and Handling","medium","conceptual",
        "What are the four necessary conditions for deadlock? How can each be prevented?",
        "Coffman conditions: (1) Mutual Exclusion — make resources sharable. (2) Hold and Wait — request all resources at once. (3) No Preemption — allow preemption. (4) Circular Wait — impose total ordering on resources. All four must hold for deadlock. Avoidance: Banker's algorithm checks safe state before granting. Detection+Recovery: kill process or preempt resource.",
        ["deadlock","os"],["OS","Amazon"])
    add(5,39,112,"Banker's Algorithm","hard","conceptual",
        "Explain the Banker's algorithm for deadlock avoidance.",
        "Banker's: check if granting resource keeps system in safe state. Safe state: there exists a sequence to complete all processes. Algorithm: Need = Max - Allocation. Simulate granting request, find safe sequence (finish all processes). If no safe sequence exists, deny request. O(n²m) where n=processes, m=resource types. Conservative: may deny safe requests.",
        ["deadlock","banker"],["OS"])
    add(5,39,112,"Mutex vs Semaphore vs Monitor","medium","conceptual",
        "Explain Mutex, Semaphore, and Monitor. When to use each?",
        "Mutex: binary lock, same thread must unlock (ownership). Binary semaphore: similar but any thread can signal. Counting Semaphore: control access to N resources. Monitor: high-level abstraction with condition variables, automatic locking. Mutex for mutual exclusion (one at a time). Semaphore for signaling/resource counting. Monitor for complex producer-consumer. Python: threading.Lock (mutex), threading.Semaphore.",
        ["synchronization","mutex","semaphore"],["OS","Amazon"])

    # Networking > URL Flow (topic=40, sub=113)
    add(5,40,113,"What Happens When You Type a URL","easy","conceptual",
        "Explain every step that happens when you type 'https://google.com' in a browser.",
        "1. DNS lookup (cache→ISP DNS→root DNS→TLD→authoritative). 2. TCP 3-way handshake. 3. TLS handshake (certificate, cipher negotiation, session key). 4. HTTP GET request. 5. Server processes request. 6. HTTP response (HTML). 7. Browser parses HTML, discovers CSS/JS/images. 8. Parallel resource fetching. 9. DOM construction + CSSOM. 10. Render tree + layout + paint.",
        ["networking","DNS","HTTP"],["Google","Amazon"])
    add(5,40,113,"DNS Resolution Process","medium","conceptual",
        "Explain recursive vs iterative DNS resolution.",
        "Recursive: client asks resolver, resolver does all work (queries root→TLD→authoritative) and returns final answer. Client gets one response. Iterative: resolver gives referral, client follows each referral. ISP resolvers use recursive for clients, iterative between DNS servers. Caching at each level. Negative caching (NXDOMAIN). DNS over HTTPS (DoH) for privacy.",
        ["DNS","networking"],["Cloudflare","Google"])
    add(5,40,113,"HTTP/1.1 vs HTTP/2 vs HTTP/3","medium","conceptual",
        "Compare HTTP versions. What problems does each solve?",
        "HTTP/1.1: persistent connections, pipelining (HOL blocking). HTTP/2: multiplexing (multiple streams on one TCP), header compression (HPACK), server push, binary protocol. Solves HOL at application layer. HTTP/3: QUIC over UDP, eliminates TCP HOL blocking, faster connection (0-RTT), built-in TLS. Mobile-friendly (no retransmission on IP change). Used by: Google, Facebook.",
        ["HTTP","networking"],["Google","Cloudflare"])
    add(5,40,113,"SSL/TLS Handshake","hard","conceptual",
        "Explain the TLS 1.3 handshake. What is forward secrecy?",
        "TLS 1.3 handshake: (1) ClientHello (supported ciphers, key share). (2) ServerHello (chosen cipher, key share, certificate, Finished). (3) Client verifies cert, sends Finished. Done in 1 RTT. Forward Secrecy: use ephemeral keys (ECDHE). Even if server private key is compromised later, past sessions can't be decrypted. TLS 1.2 required 2 RTT. 0-RTT resumption in TLS 1.3 (risk: replay attacks).",
        ["TLS","security","networking"],["Cloudflare","Amazon"])

    # Networking > TCP vs UDP (topic=40, sub=114)
    add(5,40,114,"TCP vs UDP Comparison","easy","conceptual",
        "Compare TCP and UDP. When would you choose each?",
        "TCP: connection-oriented, reliable, ordered, flow control, congestion control, higher overhead. UDP: connectionless, no reliability guarantees, faster, lower overhead. TCP use cases: HTTP, database queries, file transfer, email — where data integrity critical. UDP use cases: video streaming, gaming, DNS, VoIP — where speed > reliability. QUIC: UDP + reliability at application layer.",
        ["TCP","UDP","networking"],["Amazon","Google"])
    add(5,40,114,"TCP 3-Way Handshake","easy","conceptual",
        "Explain the TCP 3-way handshake and 4-way termination.",
        "Handshake: (1) SYN (client→server, ISN_c). (2) SYN-ACK (server→client, ISN_s, ACK ISN_c+1). (3) ACK (client→server, ISN_s+1). Connection established. Termination (4-way): (1) FIN from initiator. (2) ACK. (3) FIN from other side. (4) ACK. TIME_WAIT state (2*MSL) prevents stale packets. SYN flood attack: fill SYN queue. Mitigation: SYN cookies.",
        ["TCP","networking"],["Amazon","Google"])
    add(5,40,114,"TCP Flow Control and Congestion Control","hard","conceptual",
        "Explain TCP flow control vs congestion control. How do they work?",
        "Flow control: prevents sender from overwhelming receiver. Receiver advertises window size (rwnd). Sender limits data in flight to rwnd. Sliding window protocol. Congestion control: prevents overwhelming network. Algorithms: Slow Start (exponential growth), Congestion Avoidance (linear), Fast Retransmit, Fast Recovery. cwnd (congestion window). Cubic, BBR (Google) modern algorithms.",
        ["TCP","congestion","networking"],["Google","Cloudflare"])
    add(5,40,114,"UDP Reliability Patterns","medium","conceptual",
        "How can you build reliability over UDP? What patterns are used?",
        "Application-layer reliability over UDP: (1) Sequence numbers for ordering and duplicate detection. (2) ACKs + timeout retransmission. (3) Selective ACK (SACK). (4) ARQ protocols (Stop-and-Wait, Go-Back-N, Selective Repeat). Used in: QUIC (Google), RTP for video, game engines (position sync with delta compression). Trade-off: custom reliability = custom complexity.",
        ["UDP","reliability","networking"],["Google","Epic Games"])
    add(5,40,114,"Network Sockets Programming","medium","coding",
        "Explain how TCP sockets work. Write a minimal Python TCP server.",
        "socket() → bind(addr, port) → listen() → accept() (blocks, returns client socket) → recv/send → close(). Client: socket() → connect(server) → send/recv. Each accept() returns new socket for that client. Thread/async per connection. UDP: sendto/recvfrom, no connect/accept. Python: import socket; s=socket.socket(); s.bind(('',8080)); s.listen().",
        ["TCP","sockets","networking"],["Amazon","Google"])

    # Networking > REST (topic=40, sub=115)
    add(5,40,115,"REST API Design Principles","easy","conceptual",
        "What are the 6 REST constraints? How do they affect API design?",
        "REST constraints: (1) Client-Server separation. (2) Stateless (no session on server). (3) Cacheable (responses declare cacheability). (4) Uniform Interface (resource-based URIs, HTTP verbs, HATEOAS). (5) Layered System (client can't tell if directly connected). (6) Code on Demand (optional, send JS). RESTful API: /users (GET=list, POST=create), /users/{id} (GET/PUT/DELETE).",
        ["REST","API","networking"],["Amazon","Google"])
    add(5,40,115,"HTTP Status Codes","easy","conceptual",
        "Explain the key HTTP status code categories and common codes.",
        "2xx Success: 200 OK, 201 Created, 204 No Content. 3xx Redirect: 301 Permanent, 302 Temporary, 304 Not Modified. 4xx Client Error: 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 429 Too Many Requests. 5xx Server Error: 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable, 504 Timeout.",
        ["HTTP","REST"],["Amazon","TCS"])
    add(5,40,115,"REST vs GraphQL vs gRPC","medium","conceptual",
        "Compare REST, GraphQL, and gRPC. When would you choose each?",
        "REST: simple, cacheable, widely supported, multiple round trips for complex data. GraphQL: client specifies exact data needed, single endpoint, reduces over-fetching, N+1 query problem, less cacheable. gRPC: binary Protocol Buffers, strongly typed, bidirectional streaming, excellent for microservices. Choose REST for public APIs, GraphQL for flexible client needs, gRPC for internal microservices.",
        ["REST","GraphQL","gRPC"],["Facebook","Google"])
    add(5,40,115,"API Authentication Methods","medium","conceptual",
        "Compare API Key, JWT, OAuth 2.0, and Session-based authentication.",
        "API Key: simple, static, easy to leak. Session: server stores state, CSRF risk, doesn't scale horizontally. JWT: stateless, self-contained (user info in token), no DB lookup, can't invalidate before expiry. OAuth2: delegation protocol (grant app limited access to your account). JWT often used as OAuth2 token. PKCE for mobile. Refresh tokens for long-lived sessions.",
        ["auth","security","REST"],["Auth0","Amazon"])

    # =========================================================
    # MACHINE LEARNING — subject_id=6
    # =========================================================

    # Fundamentals (topic=41, sub=116)
    add(6,41,116,"Bias-Variance Tradeoff","medium","conceptual",
        "Explain the bias-variance tradeoff. How does model complexity affect each?",
        "Bias: error from wrong assumptions (underfitting, high bias = too simple). Variance: error from sensitivity to training data fluctuations (overfitting, high variance = too complex). Total Error = Bias² + Variance + Irreducible noise. Tradeoff: increasing complexity reduces bias but increases variance. Optimal: sweet spot in middle. Validation curve shows this.",
        ["bias_variance","ml","fundamentals"],["Google","Amazon"])
    add(6,41,116,"Supervised vs Unsupervised Learning","easy","conceptual",
        "Compare supervised, unsupervised, and reinforcement learning with examples.",
        "Supervised: labeled data, learn mapping input→output. Classification (spam), Regression (house price). Unsupervised: no labels, find patterns. Clustering (K-Means), Dimensionality reduction (PCA), Anomaly detection. Semi-supervised: few labels + many unlabeled. Reinforcement: agent learns from rewards. Self-supervised: labels from data itself (BERT, GPT predict next token).",
        ["ml","supervised","unsupervised"],["Google","Amazon"])
    add(6,41,116,"Feature Engineering Techniques","medium","conceptual",
        "What feature engineering techniques are important for ML models?",
        "Numerical: normalization (MinMax), standardization (Z-score), log transform (skewed), binning, polynomial features. Categorical: one-hot encoding (low cardinality), label encoding (ordinal), target encoding, embeddings (high cardinality). Text: TF-IDF, word2vec, BERT embeddings. Missing values: mean/median/mode imputation, indicator column, model-based. Feature selection: correlation, mutual information, recursive elimination.",
        ["feature_engineering","ml"],["Kaggle","Amazon"])
    add(6,41,116,"Cross-Validation Strategies","medium","conceptual",
        "Explain k-fold cross-validation. What are its variants and when to use them?",
        "K-fold: split into k folds, train on k-1, validate on 1, rotate. Average k scores. Reduces variance of estimate. Stratified K-fold: maintains class distribution per fold (classification). Leave-One-Out: k=n, high variance, expensive. Time Series: no shuffle, forward walk validation. Nested CV: hyperparameter tuning + evaluation. Use CV for model selection and final performance estimate.",
        ["cross_validation","ml"],["Kaggle","Google"])

    # Regularization (topic=42, sub=117)
    add(6,42,117,"L1 vs L2 Regularization","medium","conceptual",
        "Compare L1 (Lasso) and L2 (Ridge) regularization. When to use each?",
        "L1 (Lasso): adds sum(|weights|) to loss. Sparse solutions (drives some weights to exactly 0). Automatic feature selection. Unstable when features correlated. L2 (Ridge): adds sum(weights²). Spreads weight across correlated features. Doesn't zero out weights. ElasticNet: L1+L2 combined. Use L1 for sparse data/feature selection, L2 for correlated features, ElasticNet for both.",
        ["regularization","ml"],["Kaggle","Google"])
    add(6,42,117,"Dropout Regularization","medium","conceptual",
        "How does dropout work in neural networks? Why is it effective?",
        "Dropout: randomly set fraction p of neurons to 0 during each training step. Each pass sees different network architecture. Reduces co-adaptation of neurons. Ensemble effect: averages over 2^n subnetworks. During inference: scale weights by (1-p). Effective for: dense layers (not convolution). Inverted dropout: scale by 1/(1-p) during training. Modern: use BatchNorm + lower dropout.",
        ["dropout","regularization","neural_networks"],["Keras","PyTorch"])
    add(6,42,117,"Early Stopping and Learning Rate Scheduling","medium","conceptual",
        "Explain early stopping and common learning rate scheduling strategies.",
        "Early stopping: monitor validation loss, stop training when it stops improving (patience parameter). Prevents overfitting without regularization penalty. Learning rate scheduling: Step decay (reduce by factor every N epochs), Exponential decay, Cosine annealing (cyclical), Warmup (gradual increase then decay). Cyclical LR can escape local minima. OneCycleLR popular for transformers.",
        ["regularization","training","lr_schedule"],["PyTorch","Fast.ai"])
    add(6,42,117,"Batch Normalization","hard","conceptual",
        "How does Batch Normalization work? What problem does it solve?",
        "BatchNorm: normalize activations within a mini-batch to zero mean, unit variance, then scale/shift with learned γ,β. Solves internal covariate shift (distribution of inputs to layers changing during training). Benefits: allows higher learning rates, acts as regularization, reduces initialization sensitivity. During inference: use running mean/variance from training. LayerNorm (NLP): normalize across features, not batch.",
        ["batch_norm","neural_networks"],["Google","PyTorch"])

    # Evaluation (topic=43, sub=118)
    add(6,43,118,"Precision, Recall, F1 Score","easy","conceptual",
        "Explain precision, recall, F1 score, and when to optimize each.",
        "Precision = TP/(TP+FP): of all predicted positives, how many are correct. High precision → few false alarms. Recall = TP/(TP+FN): of all actual positives, how many did we find. High recall → few missed cases. F1 = 2*P*R/(P+R): harmonic mean, balance between P and R. Optimize Recall: cancer detection (don't miss cases). Precision: spam filter (don't flag legit email). F-beta: weighted if one more important.",
        ["evaluation","classification","ml"],["Google","Kaggle"])
    add(6,43,118,"ROC AUC Explained","medium","conceptual",
        "What is the ROC curve and AUC? How do you interpret them?",
        "ROC: plots TPR (recall) vs FPR at different thresholds. AUC (Area Under Curve): probability that model ranks random positive higher than random negative. AUC=1: perfect, AUC=0.5: random. Independent of threshold. Use when: class imbalance, comparing models, threshold-independent evaluation. PR curve (Precision-Recall): better for very imbalanced datasets. Average Precision (AP) = area under PR curve.",
        ["evaluation","ROC","AUC","ml"],["Kaggle","Amazon"])
    add(6,43,118,"Handling Class Imbalance","medium","conceptual",
        "What techniques handle class imbalance in classification?",
        "Data-level: SMOTE (synthetic minority oversampling), random undersampling, combination. Algorithm-level: class_weight parameter, cost-sensitive learning. Threshold moving: adjust decision threshold post-training. Ensemble: BalancedBaggingClassifier. Metric choice: use AUC-PR, F1 instead of accuracy. Collect more minority class data if possible. For extreme imbalance: anomaly detection approach.",
        ["imbalance","classification","ml"],["Kaggle","Amazon"])
    add(6,43,118,"Mean Absolute Error vs RMSE","easy","conceptual",
        "Compare MAE, MSE, and RMSE. When would you prefer each?",
        "MAE: mean absolute error. Robust to outliers. Interpretable (same units). MSE: mean squared error. Penalizes large errors more. Differentiable everywhere. RMSE: sqrt(MSE). Same units as target. Sensitive to outliers (squared). Huber loss: MAE for small errors, MSE for large — best of both. Choose RMSE when large errors are very costly. MAE for robust, outlier-heavy data.",
        ["evaluation","regression","metrics"],["Kaggle"])

    # Algorithms (topic=44, sub=119)
    add(6,44,119,"Gradient Descent Variants","medium","conceptual",
        "Compare Batch, Stochastic, and Mini-Batch Gradient Descent.",
        "Batch GD: uses all data per update. Stable convergence, slow for large data. SGD: one sample per update. Fast, noisy, can escape local minima. Mini-batch: N samples per update (N=32-512). Balance: hardware-efficient (GPU batching), stable. Adam: adaptive learning rates per parameter, momentum. AdaGrad: accumulates squared gradients. RMSProp: exponential moving average. Adam most popular.",
        ["gradient_descent","optimization","ml"],["PyTorch","Google"])
    add(6,44,119,"Decision Trees and Random Forests","medium","conceptual",
        "How do decision trees work? What makes Random Forest better?",
        "Decision Tree: recursively split on feature that maximizes information gain (Gini/entropy). Prone to overfitting. Random Forest: ensemble of trees trained on random bootstrap samples and random feature subsets. Reduces variance via averaging. Feature importance from average impurity reduction. XGBoost/LightGBM: boosting (sequential, focus on errors). RF: bagging (parallel, independent trees).",
        ["decision_tree","random_forest","ml"],["Kaggle","Amazon"])
    add(6,44,119,"K-Means Clustering","medium","conceptual",
        "Explain K-Means algorithm. What are its limitations and alternatives?",
        "K-Means: (1) Initialize k centroids. (2) Assign each point to nearest centroid. (3) Recompute centroids as cluster mean. (4) Repeat until convergence. O(n*k*iterations). Limitations: must choose k (Elbow method, Silhouette score), assumes spherical clusters, sensitive to initialization (K-Means++ fixes), outlier sensitive. Alternatives: DBSCAN (arbitrary shape, finds outliers), GMM (probabilistic, soft assignment), Agglomerative.",
        ["clustering","kmeans","ml"],["Kaggle","Google"])
    add(6,44,119,"Support Vector Machines","hard","conceptual",
        "Explain SVM. What is the kernel trick and when would you use SVM?",
        "SVM: find hyperplane maximizing margin between classes. Support vectors: closest points to hyperplane. Hard margin (linearly separable) vs soft margin (C parameter: allows misclassification). Kernel trick: map to higher-dimensional space without explicitly computing transformation. Kernels: RBF (Gaussian), polynomial, sigmoid. Good for: small datasets, high-dimensional (text), when n_features >> n_samples. Bad for: large datasets, noisy labels.",
        ["SVM","ml","kernel"],["sklearn","Amazon"])

    # Neural Networks (topic=45, sub=120)
    add(6,45,120,"Backpropagation Explained","hard","conceptual",
        "Explain backpropagation mathematically. What is the chain rule's role?",
        "Backprop: compute gradients of loss w.r.t. each weight via chain rule. Forward pass: compute outputs layer by layer. Backward pass: ∂L/∂W = ∂L/∂output * ∂output/∂W (chain rule). Gradient flows backward through layers. Vanishing gradient: deep networks, sigmoid saturates (gradient≈0). Fix: ReLU, BatchNorm, residual connections. Exploding gradient: clip gradients. Modern frameworks (PyTorch) use autograd.",
        ["backprop","neural_networks","optimization"],["PyTorch","Google"])
    add(6,45,120,"Activation Functions","medium","conceptual",
        "Compare sigmoid, ReLU, Leaky ReLU, and GELU activation functions.",
        "Sigmoid: (0,1) output, saturates at extremes (vanishing gradient), use for output layer. Tanh: (-1,1), better than sigmoid (zero-centered) but still saturates. ReLU: max(0,x), fast, no saturation for positive, dying ReLU problem (neurons stuck at 0). Leaky ReLU: α*x for x<0, fixes dying ReLU. GELU: smooth, probabilistic, used in BERT/GPT. Swish: x*sigmoid(x). GELU/Swish for transformers.",
        ["activation","neural_networks"],["PyTorch","TensorFlow"])
    add(6,45,120,"Optimizer Comparison","medium","conceptual",
        "Compare SGD with momentum, Adam, AdaGrad, and RMSProp optimizers.",
        "SGD+Momentum: accumulates velocity in consistent gradient directions, dampens oscillations. Good final performance but needs tuning. AdaGrad: adapt LR per parameter (divide by sqrt of sum of squared gradients). Good for sparse features. Decays too aggressively. RMSProp: exponential moving average of squared gradients. Fixes AdaGrad decay. Adam: momentum + RMSProp + bias correction. Works well out of box. AdamW: Adam + weight decay.",
        ["optimizers","neural_networks","training"],["PyTorch","Keras"])

    # CNN (topic=45, sub=121)
    add(6,45,121,"Convolutional Neural Networks Explained","easy","conceptual",
        "Explain CNNs. What makes them suited for image data?",
        "CNN: uses convolutional layers that apply learnable filters. Parameter sharing: same filter applied across all positions (translation invariance). Local connectivity: each neuron connects to small region. Pooling: reduce spatial dimensions, increase receptive field. Architecture: Conv→ReLU→Pool layers + Fully Connected at end. Suited for images: spatial hierarchy of features (edges→textures→shapes→objects). Much fewer params than fully connected.",
        ["CNN","computer_vision"],["Google","Facebook"])
    add(6,45,121,"CNN Architecture Evolution","medium","conceptual",
        "Describe the evolution of CNN architectures from AlexNet to ResNet.",
        "AlexNet (2012): 8 layers, ReLU, dropout, GPU training, ImageNet winner. VGG (2014): deeper (16-19 layers), 3x3 convolutions. Inception/GoogLeNet: inception modules (parallel conv at different scales). ResNet (2015): residual connections (skip connections), solved vanishing gradient, 152 layers. DenseNet: all layers connected. EfficientNet: scaled width/depth/resolution jointly. ViT: attention instead of convolution.",
        ["CNN","architecture","computer_vision"],["Google","Microsoft"])
    add(6,45,121,"ResNet and Skip Connections","hard","conceptual",
        "How do ResNet's skip connections solve the vanishing gradient problem?",
        "ResNet introduces F(x)+x residual connections. Network learns residual mapping F(x) instead of H(x). If F(x)=0, acts as identity (easy to learn). Skip connections: gradient highways — backprop flows through shortcut without degradation. Enables training 100+ layer networks. Each residual block: Conv→BN→ReLU→Conv→BN + skip. Batch Norm critical for stability. Pre-activation ResNet: BN→ReLU before conv.",
        ["CNN","ResNet","deep_learning"],["Microsoft","Google"])
    add(6,45,121,"Object Detection: YOLO vs R-CNN","hard","conceptual",
        "Compare YOLO and R-CNN approaches to object detection.",
        "R-CNN: region proposals (selective search) then classify each. Slow (2000 proposals). Fast R-CNN: shared CNN for all proposals. Faster R-CNN: Region Proposal Network (end-to-end). YOLO: single pass, divide image into grid, predict bboxes+classes per cell. Real-time (45fps). SSD: similar single-shot. YOLO better for speed, Faster R-CNN for accuracy. YOLO v8/v9 state-of-the-art.",
        ["CNN","object_detection","YOLO"],["Google","Tesla"])
    add(6,45,121,"CNN for Non-Image Tasks","medium","conceptual",
        "How are CNNs applied to text and time series data?",
        "Text CNN: 1D convolutions over word embeddings. Different kernel sizes (2,3,4 words) capture n-gram features. Pooling over time. Fast inference, good for sentence classification. Time series: 1D conv captures local temporal patterns. Better than RNN for fixed-length patterns. WaveNet: dilated causal convolutions for audio generation. Conv1D in Keras. Before transformers, CNNs competitive with RNNs for text.",
        ["CNN","NLP","time_series"],["Google","Baidu"])

    # Transformers (topic=45, sub=122)
    add(6,45,122,"Self-Attention Mechanism","hard","conceptual",
        "Explain the self-attention mechanism in transformers.",
        "Self-attention: each token attends to all other tokens. Q=query, K=key, V=value matrices from input. Attention = softmax(QK^T/√d_k)V. Scores measure relevance between all pairs. Multi-head: run h attention heads in parallel, concatenate. Captures long-range dependencies unlike RNNs. O(n²) complexity (quadratic in sequence length). Efficient variants: Longformer (sparse), Linformer (low-rank).",
        ["transformers","attention","deep_learning"],["Google","OpenAI"])
    add(6,45,122,"BERT vs GPT Architecture","medium","conceptual",
        "Compare BERT and GPT architectures. What are their use cases?",
        "BERT: bidirectional transformer encoder. Pre-trained with MLM (masked language modeling) and NSP. Good for: classification, NER, question answering (fine-tune). GPT: autoregressive decoder. Pre-trained to predict next token. Good for: text generation, few-shot prompting. BERT sees full context, GPT left-to-right only. T5: encoder-decoder, frames all NLP as text-to-text. RoBERTa: improved BERT training.",
        ["transformers","BERT","GPT"],["Google","OpenAI"])
    add(6,45,122,"Positional Encoding in Transformers","medium","conceptual",
        "Why do transformers need positional encoding? How does it work?",
        "Transformers process tokens in parallel (no sequential order). Without positional info, 'dog bites man' = 'man bites dog'. Positional encoding adds position information. Sinusoidal: PE(pos,i)=sin/cos(pos/10000^(2i/d)). Learned embeddings (BERT). Relative PE (RoPE in LLaMA): encodes relative positions in attention. ALiBi: linear bias to attention scores. Critical for sequence understanding.",
        ["transformers","positional_encoding"],["Google","Meta"])
    add(6,45,122,"Fine-tuning vs Prompting","medium","conceptual",
        "When would you fine-tune an LLM versus use prompt engineering?",
        "Fine-tuning: update model weights on task-specific data. Better for: specific domain (medical, legal), custom formats, when many examples available, consistent behavior needed. Prompting: no training, quick iteration, flexible. Few-shot: provide examples in prompt. Chain-of-thought: reasoning steps. Use prompting first (cheaper). Fine-tune when prompting insufficient. PEFT/LoRA: efficient fine-tuning (update small adapter layers).",
        ["fine_tuning","LLM","transformers"],["OpenAI","HuggingFace"])

    # LLMs (topic=46, sub=123)
    add(6,46,123,"RAG - Retrieval Augmented Generation","hard","conceptual",
        "Explain RAG architecture. What problem does it solve?",
        "RAG: enhance LLM with external knowledge retrieval. Problem: LLMs have training cutoff, hallucinate facts, context window limits. RAG: (1) Encode query + documents as vectors. (2) Retrieve top-k relevant chunks (cosine similarity). (3) Inject into LLM prompt. (4) Generate answer grounded in retrieved context. Vector DBs: FAISS, Pinecone, ChromaDB, Weaviate. Chunking strategy critical. Reranking improves precision.",
        ["RAG","LLM","embeddings"],["OpenAI","Amazon"])
    add(6,46,123,"LoRA and PEFT Techniques","hard","conceptual",
        "Explain LoRA for efficient fine-tuning of large language models.",
        "LoRA: Low-Rank Adaptation. Instead of updating all W, decompose update as W' = W + BA where B∈R^(d×r), A∈R^(r×k), r<<d. Only train A and B (much fewer params). Original weights frozen. Rank r=8 vs full rank 4096 → 99.8% param reduction. Merge at inference: no latency overhead. QLoRA: quantize base model to 4-bit, add LoRA. Train 65B model on single GPU.",
        ["LoRA","fine_tuning","LLM"],["HuggingFace","Meta"])
    add(6,46,123,"LLM Evaluation Metrics","medium","conceptual",
        "How do you evaluate the quality of LLM outputs?",
        "Automatic metrics: BLEU (n-gram overlap, translation), ROUGE (recall, summarization), BERTScore (semantic similarity). Human eval: preferred for open-ended. LLM-as-judge: GPT-4 evaluates outputs. MMLU: knowledge benchmark. HumanEval: code generation. Faithfulness (does output match context), Relevance, Coherence for RAG. Perplexity: how well model predicts next token (lower=better). G-Eval framework.",
        ["LLM","evaluation","NLP"],["OpenAI","Google"])
    add(6,46,123,"Attention is All You Need - Key Innovations","hard","conceptual",
        "What were the key innovations in the original Transformer paper?",
        "1. Self-attention: capture all pairwise relationships O(1) vs RNN's O(n). 2. Multi-head attention: multiple attention perspectives. 3. Positional encoding: sinusoidal, injected into embeddings. 4. Feed-forward sublayer after attention. 5. Residual connections + Layer Norm. 6. Encoder-decoder architecture for translation. Eliminated recurrence entirely. Foundation of all modern LLMs. 2017 paper with 100k+ citations.",
        ["transformers","attention","research"],["Google","OpenAI"])

    # =========================================================
    # BEHAVIORAL — subject_id=7
    # =========================================================

    # Self Introduction (topic=47, sub=124)
    add(7,47,124,"Tell Me About Yourself","easy","behavioral",
        "Give a structured self-introduction for a software engineer role.",
        "Structure: Present (current role, key technologies) → Past (education, relevant projects, key achievements) → Future (why this role, what you want to build). Keep to 2 minutes. Tailor to the company. Lead with most relevant experience. End with enthusiasm for the specific role. Practice until natural, not memorized.",
        ["introduction","behavioral"],["Amazon","Google"])
    add(7,47,124,"Why This Company?","easy","behavioral",
        "How do you answer 'Why do you want to work at [Company]?' authentically?",
        "Structure: (1) Specific product/mission you're excited about (show you've done research). (2) How your skills align with their tech challenges. (3) Growth opportunity specific to you. Avoid: salary, vague 'great company'. Do research: read engineering blog, recent news, talk to employees, understand their tech stack. Be specific: 'Your work on large-scale distributed systems aligns with...'",
        ["introduction","behavioral"],["Amazon","Google"])
    add(7,47,124,"Walk Me Through Your Resume","easy","behavioral",
        "How do you effectively walk an interviewer through your resume?",
        "Hit key highlights only (2-3 mins). Narrative arc: how each experience built toward this role. Quantify: 'reduced latency by 40%' not 'improved performance'. Show progression. Be ready to dive deep on any item. Match their needs: emphasize experience most relevant to JD. End: 'That brings me to here, where I'm excited about [specific opportunity]'.",
        ["introduction","resume","behavioral"],["Amazon","Microsoft"])
    add(7,47,124,"Handling Employment Gaps","medium","behavioral",
        "How do you address employment gaps in an interview?",
        "Be honest and brief. Frame positively: 'I took time to [care for family/travel/upskill/freelance]'. If learning: mention what you built or courses. Show you stayed current (open source, personal projects). Don't apologize. Address before they ask if gap is recent/large. Interviewers care more about what you'd bring than the gap. Pivot quickly to why you're ready now.",
        ["introduction","behavioral"],["Amazon"])

    # Self Assessment (topic=48, sub=125)
    add(7,48,125,"What is Your Greatest Weakness?","easy","behavioral",
        "How do you answer 'What is your greatest weakness?' authentically?",
        "Pick a real weakness that's not core to the job. Show self-awareness and active improvement. Structure: State weakness → Impact you noticed → Steps taken to improve → Current status. Examples: 'I used to underestimate estimation uncertainty. I now build in buffer and communicate risks early.' Avoid: 'I work too hard.' or 'I'm a perfectionist.'",
        ["self_assessment","behavioral"],["Amazon","Google"])
    add(7,48,125,"Describe Your Management Style","medium","behavioral",
        "How would you describe your working/collaboration style?",
        "Be honest, but align with their culture. Include: how you communicate, how you handle disagreement, your feedback style, how you work under pressure, your planning approach. Example: 'I prefer async communication for deep work but value sync discussions for complex decisions. I appreciate direct feedback and give it clearly but constructively.' Show flexibility.",
        ["self_assessment","behavioral"],["Amazon","Microsoft"])
    add(7,48,125,"How Do You Handle Pressure?","medium","behavioral",
        "Give an example of how you handle high-pressure situations.",
        "STAR format. Situation: high-stakes deadline/incident. Task: your responsibility. Action: how you prioritized, communicated, stayed focused, broke down the problem. Result: outcome. Emphasize: systematic approach under pressure, communication to stakeholders, learning from it. Show you don't panic but don't pretend pressure doesn't affect you.",
        ["self_assessment","behavioral"],["Amazon","Google"])
    add(7,48,125,"Technical Leadership Strengths","medium","behavioral",
        "What are your strengths as a technical team member or lead?",
        "Be specific and confident. Pick 2-3 backed by evidence. Examples: 'I'm strong at breaking ambiguous problems into executable steps — in [project] I...', 'I communicate technical concepts clearly to non-technical stakeholders — I once...', 'I prioritize ruthlessly under constraints — when we had to cut scope...'. Connect each to business impact.",
        ["self_assessment","behavioral"],["Amazon","Google"])

    # STAR Method (topic=49, sub=126)
    add(7,49,126,"STAR Method Explained","easy","behavioral",
        "Explain the STAR method for behavioral interviews. Give a template.",
        "STAR: Situation (set context briefly), Task (your specific responsibility), Action (what YOU did — use 'I' not 'we', specific steps), Result (measurable outcome, business impact). Tips: prep 8-10 STAR stories. Same story can answer multiple questions. Result must be quantified ('reduced by 30%', 'shipped 2 weeks early'). Keep under 3 minutes total.",
        ["STAR","behavioral"],["Amazon","Google"])
    add(7,49,126,"Tell Me About a Technical Challenge","medium","behavioral",
        "How do you structure a 'Tell me about a challenging technical problem' answer?",
        "STAR: Situation (project context, stakes). Task (your responsibility). Action (your approach: how you diagnosed, tools used, alternatives considered, why chosen approach, obstacles overcome). Result (outcome + what you learned). Depth matters: interviewers probe. Show: debugging process, systematic thinking, communication during crisis. Avoid vague 'it was complex' — give specific technical details.",
        ["STAR","behavioral","technical"],["Amazon","Google"])
    add(7,49,126,"When You Disagreed With Your Manager","hard","behavioral",
        "Describe a time you disagreed with your manager. How did you handle it?",
        "STAR. Show: professional disagreement, data-driven arguments, active listening, willingness to commit even if overruled. Structure: clearly stated your view and evidence, heard their reasoning, found common ground or agreed to disagree with commitment. Result: either outcome and what you learned. Avoid: making manager look bad, showing bitterness about outcome.",
        ["STAR","conflict","behavioral"],["Amazon","Microsoft"])
    add(7,49,126,"Most Impactful Project","medium","behavioral",
        "Describe the most impactful project you've worked on.",
        "Pick project with clear business impact and technical challenge. STAR format with emphasis on YOUR specific contributions. Quantify: users impacted, revenue affected, performance improvement, cost reduction. Include: key technical decisions you made, trade-offs, what you'd do differently. Show ownership from design to deployment to monitoring. Align impact with company's mission.",
        ["STAR","project","behavioral"],["Amazon","Google"])

    # Teamwork (topic=50, sub=127)
    add(7,50,127,"Conflict Resolution Example","medium","behavioral",
        "Describe a time you resolved a conflict within your team.",
        "STAR. Types: technical disagreement, priority conflict, communication breakdown. Actions: scheduled 1:1 to understand their perspective first, found shared goal, presented data, involved manager if needed, found compromise. Result: relationship maintained, project succeeded. Show: emotional intelligence, seeking to understand before judging, focusing on the problem not the person.",
        ["conflict","teamwork","behavioral"],["Amazon","Google"])
    add(7,50,127,"Working With Difficult Team Members","medium","behavioral",
        "How do you work effectively with a difficult team member?",
        "STAR. Define 'difficult': different work style, poor communication, blocking progress. Actions: (1) Understand their constraints/perspective first. (2) Direct private conversation: 'When X happens, I feel Y, can we try Z?' (3) Find common ground. (4) Escalate if safety/ethics issue. Result: show resolution and learning. Avoid: blaming, speaking poorly of former colleagues.",
        ["teamwork","conflict","behavioral"],["Amazon","Microsoft"])
    add(7,50,127,"Cross-Functional Collaboration","medium","behavioral",
        "Describe working on a project with multiple teams or disciplines.",
        "STAR. Emphasize: alignment techniques (shared doc, regular syncs), communication of technical decisions to non-technical stakeholders, navigating different priorities, handling dependencies. Result: shipped feature, learned other domain's constraints. Show: adaptability, clarity in communication, ability to influence without authority. Useful for: PM/design/data science collaboration.",
        ["teamwork","collaboration","behavioral"],["Amazon","Google"])
    add(7,50,127,"Mentoring and Knowledge Sharing","easy","behavioral",
        "Describe a time you mentored someone or shared knowledge with your team.",
        "STAR. Context: junior dev, new team member, code review teaching moment. Actions: pair programming, documentation, tech talk, structured feedback. Result: their growth and your leadership development. Show: investment in team's growth, patience, teaching by doing not just telling. Reflect: what you learned from teaching. Strong signal for senior roles.",
        ["teamwork","mentoring","behavioral"],["Google","Microsoft"])

    # Goals (topic=51, sub=128)
    add(7,51,128,"Where Do You See Yourself in 5 Years?","easy","behavioral",
        "How do you answer the '5 year plan' question effectively?",
        "Be genuine but align with realistic career paths at the company. Show: ambition, self-awareness, commitment to growth. Good answers: 'I want to become a strong senior engineer with deep expertise in [domain], and eventually take on technical leadership responsibilities.' Research the company's growth tracks. Show you're not just passing through. Avoid: CEO, specific titles that seem unrealistic.",
        ["goals","career","behavioral"],["Amazon","Google"])
    add(7,51,128,"Why Are You Leaving Your Current Job?","medium","behavioral",
        "How do you answer 'Why are you leaving?' professionally?",
        "Always frame positively — moving toward not away. Never badmouth previous employer. Valid reasons: seeking new challenges, want to work on [specific tech], role wasn't growing in desired direction, company direction changed. Authentic: 'I've learned a lot but want to work on problems at a larger scale.' Research their challenges so 'moving toward' feels specific and credible.",
        ["goals","behavioral"],["Amazon","Microsoft"])
    add(7,51,128,"What Motivates You at Work?","easy","behavioral",
        "What are your professional motivations? How do you answer this authentically?",
        "Self-reflect genuinely. Common motivators: solving hard problems, seeing product impact, learning new things, mentoring, building at scale, user impact. Pick what's truly authentic. Back with evidence: 'I'm most motivated by..., which is why I [took on X project, stayed late to...]. I can see this role offers...' Align with company mission. Avoid: money, job security (even if true).",
        ["goals","motivation","behavioral"],["Google","Amazon"])
    add(7,51,128,"Salary Expectations","medium","behavioral",
        "How do you handle salary expectation questions in interviews?",
        "Research first: levels.fyi, Glassdoor, LinkedIn Salary, Blind for the specific company and level. Delay: 'I'm open to discussing compensation once I know more about the full scope of the role.' Or give range: 'Based on my research for [level] in [location], I'd expect $X-Y.' Consider total comp (RSU, bonus, benefits). Don't anchor too low. BATNA: have alternatives to negotiate confidently.",
        ["goals","negotiation","behavioral"],["Amazon","Google"])

    # Failure (topic=52, sub=129)
    add(7,52,129,"Tell Me About a Failure","medium","behavioral",
        "How do you answer 'Tell me about a time you failed'?",
        "Pick a real failure with stakes (not trivial). STAR format. Emphasize: what you learned, what you changed, how you recovered. Show: accountability (no blaming), growth mindset, resilience. Strong answers: project that missed deadline, wrong technical decision, shipped bug. Structure: what went wrong → your role in it → immediate recovery → systemic fix → result. Don't end on the failure — end on the learning.",
        ["failure","behavioral","growth_mindset"],["Amazon","Google"])
    add(7,52,129,"Biggest Professional Regret","hard","behavioral",
        "How do you answer 'What is your biggest professional regret?'",
        "Honest self-reflection. Show growth mindset: you'd handle it differently now. Options: not speaking up sooner about a technical concern, not investing in team relationships, shipping without sufficient testing. Structure: situation → what happened → what I wish I'd done → what I do differently now. Demonstrates maturity and continuous learning. Keep past, focus on present improvement.",
        ["failure","regret","behavioral"],["Google","Microsoft"])
    add(7,52,129,"Learning from Mistakes","medium","behavioral",
        "How do you describe how you learn from mistakes as an engineer?",
        "Show systematic approach: (1) Acknowledge quickly, communicate to affected parties. (2) Fix the immediate issue. (3) Root cause analysis (5 Whys, blameless post-mortem). (4) Systemic fix: tests, documentation, process change. (5) Share learnings with team. Example: shipped bug → hotfix → added test coverage → documented edge case → presented to team. Culture: mistakes are learning opportunities not blame.",
        ["failure","learning","behavioral"],["Amazon","Google"])
    add(7,52,129,"Adapting to Change","medium","behavioral",
        "Describe a time you had to quickly adapt to a major change.",
        "STAR. Changes: technical direction pivot, team reorganization, new requirements, technology migration. Actions: quickly assess impact, communicate concerns with data, adapt plan, help team transition. Result: shipped despite change. Show: flexibility, leading through ambiguity, maintaining productivity during uncertainty. Avoid showing you're resistant to change. Agile mindset.",
        ["failure","adaptability","behavioral"],["Amazon","Google"])

    conn.commit()
    cur.execute("SELECT COUNT(*) FROM questions")
    total = cur.fetchone()[0]
    print(f"SUCCESS: Questions inserted successfully!")
    print(f"Total questions in database: {total}")
    cur.execute("""
        SELECT s.name, COUNT(q.id) as count
        FROM subjects s LEFT JOIN questions q ON q.subject_id = s.id
        GROUP BY s.name ORDER BY s.name
    """)
    print("\nQuestions by subject:")
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[1]}")
    conn.close()

if __name__ == "__main__":
    run()
