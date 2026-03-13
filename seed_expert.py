"""
Seed expert-level questions across all subjects.
Target: bring expert count from 20 to 45+.
"""
import psycopg2

conn = psycopg2.connect("postgresql://postgres:admin123@localhost:5432/interview_db")
cur = conn.cursor()

count = 0

def add(subject_id, topic_id, subtopic_id, title, qtype, question_text, ideal_answer):
    global count
    cur.execute("SELECT id FROM questions WHERE title=%s AND subtopic_id=%s", (title, subtopic_id))
    if cur.fetchone():
        return
    cur.execute("""
        INSERT INTO questions (subject_id, topic_id, subtopic_id, title, type, difficulty,
                               question_text, ideal_answer)
        VALUES (%s, %s, %s, %s, %s, 'expert', %s, %s)
    """, (subject_id, topic_id, subtopic_id, title, qtype, question_text, ideal_answer))
    count += 1


# ── DSA Expert Questions (subject=1) ────────────────────────────────────────

# Arrays - Expert (sub=11, topic=1)
add(1, 1, 11, "Trapping Rain Water Optimized",
    "coding",
    "Solve the Trapping Rain Water problem in O(n) time and O(1) space using the two-pointer technique.",
    "Use two pointers from both ends. Track left_max and right_max. Move the pointer with smaller max inward. Water at each position = min(left_max, right_max) - height[i]. O(n) time, O(1) space.")

add(1, 1, 11, "Median of Two Sorted Arrays",
    "coding",
    "Find the median of two sorted arrays in O(log(min(m,n))) time.",
    "Binary search on the shorter array. Partition both arrays such that left half has (m+n+1)/2 elements. Ensure maxLeft1 <= minRight2 and maxLeft2 <= minRight1. Median from the partition boundary values.")

# Graphs - Shortest Path (sub=74, topic=16)
add(1, 16, 74, "Dijkstra with Negative Edge Handling",
    "conceptual",
    "Why does Dijkstra's algorithm fail with negative edge weights? How does Bellman-Ford solve this? Compare their complexities.",
    "Dijkstra assumes relaxed nodes are final, but negative edges can reduce distances later. Bellman-Ford relaxes all edges V-1 times, handling negatives. Dijkstra: O(E log V). Bellman-Ford: O(VE). For negative cycles, Bellman-Ford detects them in Vth iteration.")

add(1, 16, 74, "A* Search Algorithm",
    "conceptual",
    "Explain the A* search algorithm. What are admissible and consistent heuristics? When is A* optimal?",
    "A* uses f(n) = g(n) + h(n) where g is actual cost and h is heuristic estimate. Admissible: h never overestimates. Consistent: h(n) <= cost(n,n') + h(n'). A* is optimal with admissible heuristic and consistent guarantees no re-expansion of nodes.")

# DP - Expert (sub=84, topic=18)
add(1, 18, 84, "Matrix Chain Multiplication",
    "coding",
    "Given dimensions of matrices, find the minimum number of multiplications needed to compute their product. Explain the DP approach.",
    "DP on chain length. dp[i][j] = min cost to multiply matrices i..j. For each split k: dp[i][j] = min(dp[i][k] + dp[k+1][j] + dims[i-1]*dims[k]*dims[j]). O(n^3) time, O(n^2) space. Bottom-up by increasing chain length.")

add(1, 18, 84, "Edit Distance Variants",
    "coding",
    "Implement edit distance with weighted operations (insert=1, delete=1, replace=2). How does this change the DP recurrence?",
    "dp[i][j] = min of: dp[i-1][j]+1 (delete), dp[i][j-1]+1 (insert), dp[i-1][j-1] + (0 if match, 2 if replace). Base cases: dp[0][j]=j, dp[i][0]=i. The higher replace cost makes the algorithm prefer insert+delete over replacement when characters differ.")

# Trees - Advanced (sub=62, topic=13)
add(1, 13, 62, "Segment Tree with Lazy Propagation",
    "coding",
    "Explain segment trees with lazy propagation. When is it needed? Give the time complexity for range update and range query.",
    "Segment tree stores aggregate values for intervals. Lazy propagation defers updates to children until needed. Range update: mark lazy flag, push down on query. Both range update and range query are O(log n). Used for range sum/min/max with range updates.")

# Tries - Basics (sub=85, topic=19)
add(1, 19, 85, "Implement a Trie with Wildcard Search",
    "coding",
    "Design a Trie that supports addWord and search with '.' as wildcard matching any character.",
    "Standard trie insert for addWord. For search with '.': at each '.', recursively try all 26 children. For normal chars, follow the specific child. Return true if any path reaches end-of-word. Time: O(26^m) worst case for wildcards, O(m) for normal search.")

# ── OOPS Expert Questions (subject=2) ───────────────────────────────────────

# SOLID (sub=92, topic=22)
add(2, 22, 92, "SOLID Violations in Real Code",
    "conceptual",
    "Given a class that handles user authentication, database queries, and email sending, identify which SOLID principles are violated and refactor.",
    "Violates SRP (3 responsibilities), OCP (adding auth methods requires modification), DIP (depends on concrete DB/email). Refactor: separate AuthService, UserRepository, EmailService. Use interfaces/abstractions. Each class has one reason to change.")

add(2, 22, 92, "Liskov Substitution Deep Dive",
    "conceptual",
    "Explain why Square extending Rectangle violates LSP. How would you redesign this hierarchy?",
    "Square overrides setWidth/setHeight to keep sides equal, breaking Rectangle's contract where width and height are independent. Client code expecting Rectangle behavior fails with Square. Fix: use a Shape interface with area() method. Square and Rectangle implement Shape independently without inheritance.")

# Design Patterns - Singleton (sub=93, topic=23)
add(2, 23, 93, "Thread-Safe Singleton Patterns",
    "conceptual",
    "Compare 4 ways to implement thread-safe Singleton: synchronized method, double-checked locking, eager initialization, and enum. Which is best and why?",
    "1) Synchronized method: simple but slow due to lock on every call. 2) Double-checked locking: volatile + sync block, fast but complex. 3) Eager: created at class load, simple but wastes memory if unused. 4) Enum: best - JVM guarantees single instance, handles serialization and reflection attacks. Joshua Bloch recommends enum approach.")

# ── System Design Expert Questions (subject=3) ──────────────────────────────

# Distributed Systems (sub=100, topic=28)
add(3, 28, 100, "Design a Distributed Message Queue",
    "system_design",
    "Design a distributed message queue like Kafka. Cover partitioning, replication, consumer groups, and exactly-once delivery.",
    "Topics partitioned across brokers. Each partition is an append-only log. Replication: leader-follower with ISR. Consumer groups: each partition consumed by one consumer per group. Exactly-once: idempotent producers + transactional writes + consumer offset commits. Retention-based, not deletion-based. ZooKeeper/KRaft for coordination.")

add(3, 28, 100, "Design a Real-Time Analytics Pipeline",
    "system_design",
    "Design a system to process 1M events/second for real-time dashboards. Cover ingestion, processing, storage, and querying.",
    "Ingestion: Kafka with partitioning by event type. Processing: Flink/Spark Streaming for windowed aggregations. Storage: time-series DB (InfluxDB) for metrics, Elasticsearch for search. Pre-computed materialized views for dashboards. Lambda architecture: batch for accuracy, stream for speed. Query: GraphQL API with caching layer.")

# Scalability (sub=96, topic=24)
add(3, 24, 96, "Horizontal vs Vertical Scaling Trade-offs",
    "system_design",
    "Compare horizontal and vertical scaling. When would you choose each? Discuss cost, complexity, and failure modes.",
    "Vertical: simpler, no distributed complexity, limited by hardware ceiling, single point of failure. Horizontal: infinite scale, needs load balancing/sharding/distributed state, more complex but fault-tolerant. Choose vertical for stateful DBs initially, horizontal for stateless services. Cost: vertical has diminishing returns; horizontal is more cost-effective at scale.")

# ── DBMS Expert Questions (subject=4) ───────────────────────────────────────

# Distributed DB - CAP (sub=108, topic=35)
add(4, 35, 108, "CAP Theorem in Practice",
    "conceptual",
    "Explain CAP theorem with real database examples. Why is PACELC a better model? Where do MongoDB, Cassandra, and PostgreSQL fall?",
    "CAP: choose 2 of Consistency, Availability, Partition-tolerance (P is mandatory in distributed systems, so really C vs A). PACELC adds: if no Partition, choose Latency vs Consistency. MongoDB: CP (consistent reads from primary). Cassandra: AP (tunable consistency). PostgreSQL: CA (single-node) or CP (with streaming replication). PACELC better captures normal operation trade-offs.")

add(4, 35, 108, "Database Sharding Strategies",
    "conceptual",
    "Compare hash-based, range-based, and directory-based sharding. How do you handle hot spots and cross-shard queries?",
    "Hash: even distribution, poor range queries. Range: good for range scans, risk of hotspots. Directory: flexible but lookup overhead. Hotspots: consistent hashing, virtual shards, or shard splitting. Cross-shard queries: scatter-gather pattern, denormalization, or materialized views. Resharding: use virtual shards mapped to physical nodes for easier rebalancing.")

# Transactions (sub=102, topic=30)
add(4, 30, 102, "Isolation Levels and Anomalies",
    "conceptual",
    "Explain all SQL isolation levels. Map each to the anomalies it prevents: dirty read, non-repeatable read, phantom read, write skew.",
    "Read Uncommitted: no protection. Read Committed: prevents dirty reads (uses short read locks). Repeatable Read: prevents dirty + non-repeatable reads (holds read locks). Serializable: prevents all including phantoms (range locks or SSI). Write skew only prevented by serializable. PostgreSQL default: Read Committed. MySQL InnoDB default: Repeatable Read with gap locks.")

# ── OS & Networking Expert Questions (subject=5) ────────────────────────────

# Memory Management - Paging (sub=111, topic=38)
add(5, 38, 111, "Virtual Memory and Page Replacement Expert",
    "conceptual",
    "Compare LRU, Clock, and Working Set page replacement algorithms. What is Belady's anomaly and which algorithms are immune?",
    "LRU: replaces least recently used, good performance but expensive to implement exactly (needs timestamp/stack). Clock: approximation of LRU using reference bit, circular buffer. Working Set: tracks pages used in recent window, prevents thrashing. Belady's anomaly: more frames can cause more faults (FIFO suffers). Stack algorithms (LRU, Optimal) are immune.")

# Networking (sub=114, topic=40)
add(5, 40, 114, "TCP Congestion Control Deep Dive",
    "conceptual",
    "Explain TCP congestion control phases: slow start, congestion avoidance, fast retransmit, fast recovery. How does TCP CUBIC differ?",
    "Slow start: exponential growth (cwnd doubles each RTT) until ssthresh. Congestion avoidance: linear growth (cwnd += 1/cwnd per ACK). Fast retransmit: 3 duplicate ACKs trigger retransmit without timeout. Fast recovery: halve cwnd, skip slow start. TCP CUBIC: uses cubic function of time since last loss, better for high-bandwidth-delay networks. CUBIC is default in Linux.")

# CPU Scheduling (sub=110, topic=37)
add(5, 37, 110, "CFS and Real-Time Scheduling",
    "conceptual",
    "Explain Linux's Completely Fair Scheduler (CFS). How does it achieve fairness? How do real-time scheduling classes (FIFO, RR) interact with CFS?",
    "CFS uses red-black tree sorted by virtual runtime (vruntime). Process with smallest vruntime runs next. vruntime increases slower for higher-priority tasks (nice values). Time slice proportional to weight. RT classes (SCHED_FIFO, SCHED_RR) have higher priority than CFS. SCHED_FIFO: runs until yield/block. SCHED_RR: FIFO with time quantum. RT tasks always preempt normal tasks.")

# ── Machine Learning Expert Questions (subject=6) ──────────────────────────

# Neural Networks - Transformers (sub=122, topic=45)
add(6, 45, 122, "Self-Attention Mechanism Mathematics",
    "conceptual",
    "Derive the self-attention mechanism mathematically. Why scale by sqrt(d_k)? Explain multi-head attention and its benefits.",
    "Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) * V. Q,K,V are linear projections of input. Scaling by sqrt(d_k) prevents softmax saturation for large d_k (dot products grow with dimension). Multi-head: run h parallel attention heads with different projections, concatenate outputs, project again. Benefits: attends to different representation subspaces, captures diverse relationships.")

# LLMs (sub=123, topic=46)
add(6, 46, 123, "LLM Training Pipeline",
    "conceptual",
    "Explain the full LLM training pipeline: pretraining, supervised fine-tuning (SFT), and RLHF. What is DPO and how does it simplify RLHF?",
    "Pretraining: next-token prediction on massive corpus (causal LM objective). SFT: fine-tune on instruction-response pairs. RLHF: train reward model on human preferences, then optimize policy with PPO against reward model. DPO (Direct Preference Optimization): skips reward model, directly optimizes policy from preference pairs using a classification loss. DPO is simpler, more stable, and computationally cheaper than RLHF.")

add(6, 46, 123, "Inference Optimization Techniques",
    "conceptual",
    "Explain KV-cache, speculative decoding, and quantization for LLM inference. How do they reduce latency?",
    "KV-cache: store key-value pairs from previous tokens to avoid recomputation. Reduces O(n^2) to O(n) per step. Speculative decoding: small draft model generates candidates, large model verifies in parallel batch. 2-3x speedup. Quantization: reduce weights from FP16 to INT8/INT4. GPTQ, AWQ for weight-only quantization. Reduces memory 2-4x, enables larger batch sizes. Combining all three gives best throughput.")

# Evaluation - Metrics (sub=118, topic=43)
add(6, 43, 118, "Advanced ML Evaluation",
    "conceptual",
    "When is accuracy misleading? Explain precision-recall trade-off, ROC AUC vs PR AUC, and calibration. When would you use each metric?",
    "Accuracy misleading with imbalanced classes (99% majority = 99% accuracy by guessing). Precision-recall: trade-off controlled by threshold. PR AUC better for imbalanced datasets. ROC AUC measures discrimination ability, insensitive to class balance. Calibration: predicted probabilities match actual frequencies. Use Brier score or reliability diagrams. Medical: high recall (catch all positives). Spam: high precision (avoid false positives).")

# ── Behavioral Expert Questions (subject=7) ──────────────────────────────────

# Challenges (sub=126, topic=49)
add(7, 49, 126, "Leading Under Ambiguity",
    "behavioral",
    "Describe a time when you had to make a critical technical decision with incomplete information. What was your approach?",
    "Strong answer uses STAR method. Shows: 1) Identified what information was available vs missing. 2) Assessed risks of delaying vs acting. 3) Made a reversible decision where possible. 4) Set up checkpoints to validate the decision. 5) Communicated uncertainty to stakeholders. Key: demonstrate structured thinking under uncertainty, not just confidence.")

# Teamwork (sub=127, topic=50)
add(7, 50, 127, "Cross-Team Technical Alignment",
    "behavioral",
    "How would you drive alignment between two engineering teams with conflicting technical approaches to solving the same problem?",
    "1) Understand both perspectives deeply before proposing solutions. 2) Define shared evaluation criteria (performance, maintainability, timeline). 3) Propose a structured comparison (RFC, design doc, prototype). 4) Facilitate objective discussion focused on trade-offs, not preferences. 5) Escalate to architecture review if needed. 6) Document the decision and rationale for future reference.")

conn.commit()
print(f"Inserted {count} expert questions")

cur.execute("SELECT difficulty, COUNT(*) FROM questions GROUP BY difficulty ORDER BY difficulty")
print("\nFinal difficulty distribution:")
for r in cur.fetchall():
    print(f"  {r[0]}: {r[1]}")
cur.execute("SELECT COUNT(*) FROM questions")
print(f"Total: {cur.fetchone()[0]}")

conn.close()
