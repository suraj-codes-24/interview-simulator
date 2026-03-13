"""
seed_v2_dsa_fill.py — Fill thin DSA subtopics (min 3 each) + add expert questions
"""
import psycopg2

DB_URL = "postgresql://postgres:admin123@localhost:5432/interview_db"

def run():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    count = 0

    def add(subject_id, topic_id, subtopic_id, title, difficulty, qtype, question_text, ideal_answer, tags=None, companies=None):
        nonlocal count
        cur.execute("""
            INSERT INTO questions (subject_id, topic_id, subtopic_id, title, difficulty, type, question_text, ideal_answer, tags, companies)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (subject_id, topic_id, subtopic_id, title, difficulty, qtype,
              question_text, ideal_answer, tags or [], companies or []))
        count += 1

    S = 1  # DSA subject_id

    # ── Strings (topic=2) ──

    # Basics (sub=12)
    add(S,2,12,"Reverse a String","beginner","coding",
        "Write a function to reverse a string in-place.",
        "Two pointer approach: swap characters at left and right pointers, move inward. O(n) time, O(1) space. In Python: s[::-1] or list(s) then two-pointer swap.",
        ["strings","two_pointers"],["TCS"])
    add(S,2,12,"Check if String is Palindrome","beginner","coding",
        "Check if a given string reads the same forwards and backwards.",
        "Two pointers from both ends, compare characters. Skip non-alphanumeric for 'valid palindrome'. O(n) time, O(1) space.",
        ["strings","two_pointers"],["Amazon"])

    # Palindrome (sub=13)
    add(S,2,13,"Longest Palindromic Substring","intermediate","coding",
        "Find the longest palindromic substring in a given string.",
        "Expand around center: for each index, expand outward checking palindrome (odd and even length). O(n^2) time. Manacher's algorithm for O(n).",
        ["strings","palindrome","dp"],["Amazon","Google"])
    add(S,2,13,"Palindrome Partitioning","advanced","coding",
        "Partition string such that every substring is a palindrome. Return all partitions.",
        "Backtracking: at each position, try all palindrome prefixes, recurse on rest. DP precompute isPalin[i][j]. O(n * 2^n) worst case.",
        ["strings","backtracking","dp"],["Google"])

    # Anagram (sub=14)
    add(S,2,14,"Group Anagrams","intermediate","coding",
        "Given list of strings, group anagrams together.",
        "Sort each string as key for hashmap. All anagrams produce same sorted key. O(n * k log k) where k is max string length. Alt: frequency count tuple as key.",
        ["strings","hashing"],["Amazon","Google"])
    add(S,2,14,"Valid Anagram Check","beginner","coding",
        "Check if two strings are anagrams of each other.",
        "Count character frequencies in both. Compare. O(n) time. Or sort both and compare O(n log n). Hashmap/Counter approach preferred.",
        ["strings","hashing"],["Microsoft"])

    # Sliding Window on String (sub=15)
    add(S,2,15,"Minimum Window Substring","advanced","coding",
        "Find smallest window in s containing all characters of t.",
        "Sliding window with two pointers and frequency map. Expand right to include all chars. Shrink left to minimize. Track best window. O(n).",
        ["strings","sliding_window"],["Google","Facebook"])
    add(S,2,15,"Longest Substring Without Repeating","intermediate","coding",
        "Find length of longest substring without repeating characters.",
        "Sliding window with hashset. Expand right, if duplicate found shrink left until no duplicate. Track max length. O(n).",
        ["strings","sliding_window"],["Amazon"])

    # Pattern Matching (sub=16)
    add(S,2,16,"KMP Algorithm","advanced","coding",
        "Explain KMP pattern matching algorithm and its preprocessing step.",
        "Build failure function (LPS array): for each position, length of longest proper prefix that is also suffix. Match uses LPS to skip characters. O(n+m) instead of O(n*m) brute force.",
        ["strings","pattern_matching"],["Google"])
    add(S,2,16,"Rabin-Karp Algorithm","intermediate","coding",
        "Explain Rabin-Karp string matching with rolling hash.",
        "Compute hash of pattern and rolling hash of text windows. Compare hashes; on match verify character by character. O(n+m) average, O(nm) worst case with many collisions.",
        ["strings","hashing"],["Microsoft"])

    # Compression (sub=17)
    add(S,2,17,"Run Length Encoding","beginner","coding",
        "Implement run-length encoding for a string. 'aabccc' -> 'a2b1c3'.",
        "Iterate through string, count consecutive same characters. Append char + count. Handle single characters. O(n) time.",
        ["strings","compression"],["TCS","Wipro"])
    add(S,2,17,"String Compression In-Place","intermediate","coding",
        "Compress string in-place. If compressed not shorter, return original.",
        "Two pointer: read pointer scans, write pointer writes char + count. Only compress if result is shorter. O(n) time, O(1) space.",
        ["strings","two_pointers"],["Amazon"])

    # Rotation (sub=18)
    add(S,2,18,"Check if String is Rotation","beginner","coding",
        "Check if string s2 is a rotation of s1.",
        "Concatenate s1+s1 and check if s2 is a substring. 'waterbottle' is rotation of 'erbottlewat': 'erbottlewaterbottlewat' contains 'waterbottle'. O(n).",
        ["strings","rotation"],["Amazon"])
    add(S,2,18,"Rotate String by K Positions","beginner","coding",
        "Rotate string left by k positions.",
        "Reverse first k chars, reverse rest, reverse whole string. Or simply return s[k:] + s[:k]. O(n) time.",
        ["strings","rotation"],["TCS"])

    # Advanced Strings (sub=19) - already has 2
    add(S,2,19,"Longest Common Prefix","beginner","coding",
        "Find longest common prefix among array of strings.",
        "Vertical scanning: compare characters at same position across all strings. Stop when mismatch. O(S) where S is sum of all characters.",
        ["strings"],["Google"])

    # Expert Strings (sub=20)
    add(S,2,20,"Regular Expression Matching","expert","coding",
        "Implement regex matching with '.' (any char) and '*' (zero or more of preceding).",
        "2D DP: dp[i][j] = does s[:i] match p[:j]. For '*': zero occurrences dp[i][j-2] or match+repeat dp[i-1][j] if p[j-1] matches s[i]. O(m*n).",
        ["strings","dp"],["Google","Facebook"])
    add(S,2,20,"Edit Distance","expert","coding",
        "Find minimum edit operations (insert, delete, replace) to convert word1 to word2.",
        "2D DP: dp[i][j] = min edits for word1[:i] to word2[:j]. If match: dp[i-1][j-1]. Else: 1 + min(insert=dp[i][j-1], delete=dp[i-1][j], replace=dp[i-1][j-1]). O(m*n).",
        ["strings","dp"],["Amazon","Microsoft"])

    # ── Linked List (topic=3) ──

    # Basics (sub=21)
    add(S,3,21,"Reverse a Linked List","beginner","coding",
        "Reverse a singly linked list iteratively.",
        "Three pointers: prev=None, curr=head, next. Loop: next=curr.next, curr.next=prev, prev=curr, curr=next. Return prev. O(n) time, O(1) space.",
        ["linked_list"],["Amazon","Microsoft"])
    add(S,3,21,"Middle of Linked List","beginner","coding",
        "Find the middle node of a linked list.",
        "Fast-slow pointer: slow moves 1 step, fast moves 2. When fast reaches end, slow is at middle. O(n) time, O(1) space.",
        ["linked_list","fast_slow"],["Amazon"])

    # Reversal (sub=22)
    add(S,3,22,"Reverse Linked List in Groups of K","advanced","coding",
        "Reverse nodes in groups of k. If remaining < k, leave as is.",
        "Iterative: for each group, reverse k nodes, connect to previous group's tail. Track head of first group as new head. O(n) time.",
        ["linked_list","reversal"],["Amazon","Microsoft"])
    add(S,3,22,"Reverse Between Positions","intermediate","coding",
        "Reverse a linked list from position left to position right.",
        "Navigate to position left-1 (connection point). Reverse nodes from left to right. Reconnect. Handle edge case when left=1 (dummy head). O(n).",
        ["linked_list","reversal"],["Google"])

    # Cycle Detection (sub=23)
    add(S,3,23,"Find Start of Cycle","intermediate","coding",
        "Detect cycle and find the node where cycle begins.",
        "Floyd's: fast and slow meet inside cycle. Then move one pointer to head, both move 1 step. They meet at cycle start. Proof: mathematical property of distances. O(n) time, O(1) space.",
        ["linked_list","cycle","fast_slow"],["Amazon"])
    add(S,3,23,"Remove Cycle from Linked List","intermediate","coding",
        "Detect and remove a cycle from a linked list.",
        "Find cycle start using Floyd's. Then find node before cycle start (its next = cycle start). Set that node's next to null. O(n) time.",
        ["linked_list","cycle"],["Microsoft"])

    # Merge (sub=24)
    add(S,3,24,"Merge K Sorted Lists","advanced","coding",
        "Merge k sorted linked lists into one sorted list.",
        "Min-heap of size k: push first node of each list. Pop smallest, push its next. O(N log k) where N=total nodes. Alt: divide and conquer merge pairs. O(N log k).",
        ["linked_list","heap"],["Amazon","Google"])
    add(S,3,24,"Merge Two Sorted Lists","beginner","coding",
        "Merge two sorted linked lists into one sorted list.",
        "Dummy head. Compare both heads, append smaller. Move that pointer forward. When one exhausted, append remaining. O(n+m) time.",
        ["linked_list","merge"],["Amazon"])

    # Fast Slow (sub=25)
    add(S,3,25,"Palindrome Linked List","intermediate","coding",
        "Check if a singly linked list is a palindrome.",
        "Find middle (fast-slow), reverse second half, compare both halves. Restore list if needed. O(n) time, O(1) space.",
        ["linked_list","fast_slow"],["Amazon"])
    add(S,3,25,"Reorder List","intermediate","coding",
        "Reorder list L0->L1->...->Ln to L0->Ln->L1->Ln-1->...",
        "Find middle, reverse second half, interleave merge both halves. O(n) time, O(1) space. Combines three techniques.",
        ["linked_list","fast_slow"],["Amazon"])

    # Advanced LL (sub=26)
    add(S,3,26,"Clone Linked List with Random Pointer","advanced","coding",
        "Deep copy a linked list where each node has a random pointer.",
        "Interleave: insert clone after each original. Set clone.random = original.random.next. Separate lists. O(n) time, O(1) extra space. Alt: hashmap O(n) space.",
        ["linked_list"],["Amazon","Facebook"])
    add(S,3,26,"Flatten a Multilevel Linked List","intermediate","coding",
        "Flatten a doubly linked list where nodes may have child lists.",
        "DFS/stack: when child found, save next, connect child, recurse/iterate through child list, connect tail to saved next. O(n) time.",
        ["linked_list","dfs"],["Microsoft"])

    # ── Stacks (topic=4) ──

    # Basics (sub=28)
    add(S,4,28,"Implement Stack Using Array","beginner","coding",
        "Implement a stack with push, pop, peek, isEmpty using an array.",
        "Array with top pointer. Push: increment top, set arr[top]. Pop: return arr[top], decrement. Peek: return arr[top]. O(1) all ops. Handle overflow/underflow.",
        ["stack"],["TCS"])
    add(S,4,28,"Evaluate Postfix Expression","intermediate","coding",
        "Evaluate a postfix (Reverse Polish) expression using a stack.",
        "Scan left to right: if operand push. If operator pop two, compute, push result. Final stack top is answer. O(n) time.",
        ["stack"],["Amazon"])

    # Parentheses (sub=29)
    add(S,4,29,"Minimum Add to Make Parentheses Valid","intermediate","coding",
        "Find minimum additions to make a parentheses string valid.",
        "Track open and close needed. For '(': open++. For ')': if open > 0 open-- else close++. Answer = open + close. O(n).",
        ["stack","parentheses"],["Facebook"])
    add(S,4,29,"Generate All Valid Parentheses","intermediate","coding",
        "Generate all combinations of n pairs of well-formed parentheses.",
        "Backtracking: track open and close count. Add '(' if open < n. Add ')' if close < open. Base case: length = 2n. Catalan number results.",
        ["stack","backtracking"],["Amazon","Google"])

    # Monotonic Stack (sub=30)
    add(S,4,30,"Daily Temperatures","intermediate","coding",
        "For each day find how many days until warmer temperature.",
        "Monotonic decreasing stack of indices. For each temp, pop all smaller from stack and record distance. O(n) time.",
        ["stack","monotonic"],["Amazon"])
    add(S,4,30,"Next Greater Element","intermediate","coding",
        "Find next greater element for each element in array.",
        "Monotonic stack: traverse right to left. Pop all smaller or equal. Stack top is answer. Push current. O(n).",
        ["stack","monotonic"],["Amazon","Google"])

    # Histogram (sub=31)
    add(S,4,31,"Maximal Rectangle in Binary Matrix","advanced","coding",
        "Find largest rectangle containing only 1s in a binary matrix.",
        "Build histogram heights per row. Apply largest rectangle in histogram for each row. O(m*n). Reuses monotonic stack histogram solution.",
        ["stack","histogram","matrix"],["Google"])
    add(S,4,31,"Trapping Rain Water Using Stack","advanced","coding",
        "Solve trapping rain water using a monotonic stack approach.",
        "Monotonic decreasing stack. When taller bar found, pop and calculate trapped water between current and new stack top. O(n) time, O(n) space.",
        ["stack","monotonic"],["Amazon"])

    # Stack Design (sub=32)
    add(S,4,32,"Min Stack","intermediate","coding",
        "Design a stack that supports getMin in O(1) time.",
        "Two stacks: main + min stack. Push to min stack when value <= current min. Pop from min stack when popping current min. All ops O(1).",
        ["stack","design"],["Amazon","Google"])
    add(S,4,32,"Implement Queue Using Two Stacks","intermediate","coding",
        "Implement a FIFO queue using two stacks.",
        "Stack1 for enqueue, Stack2 for dequeue. On dequeue: if stack2 empty, pour all from stack1. Pop from stack2. Amortized O(1).",
        ["stack","queue","design"],["Microsoft"])

    # ── Queues (topic=5) ──

    # Basics (sub=33)
    add(S,5,33,"Implement Queue Using Array","beginner","coding",
        "Implement a circular queue using an array.",
        "Array with front and rear pointers. Enqueue: rear = (rear+1)%size. Dequeue: front = (front+1)%size. Track count for full/empty. O(1) all ops.",
        ["queue","circular"],["TCS"])
    add(S,5,33,"BFS Using Queue","beginner","coding",
        "Implement BFS traversal of a graph using a queue.",
        "Start: enqueue source, mark visited. Loop: dequeue, process, enqueue all unvisited neighbors. O(V+E). Queue ensures level-order exploration.",
        ["queue","bfs","graphs"],["Amazon"])

    # Sliding Window Queue (sub=34)
    add(S,5,34,"Sliding Window Maximum Using Deque","advanced","coding",
        "Find max in every window of size k using a deque.",
        "Monotonic decreasing deque of indices. For each element: remove from back if smaller. Remove from front if out of window. Front is always max. O(n).",
        ["queue","deque","sliding_window"],["Amazon","Google"])
    add(S,5,34,"First Negative in Window","intermediate","coding",
        "Find first negative number in every window of size k.",
        "Queue of indices of negative numbers. For each window, front of queue is answer if in range. O(n).",
        ["queue","sliding_window"],["Microsoft"])

    # Queue Design (sub=35)
    add(S,5,35,"Design Circular Deque","intermediate","coding",
        "Design a double-ended circular queue with insertFront/Rear, deleteFront/Rear.",
        "Array with front, rear pointers. InsertFront: front=(front-1+cap)%cap. InsertRear: rear=(rear+1)%cap. Track size. All O(1).",
        ["queue","design"],["Amazon"])
    add(S,5,35,"Implement Stack Using Queues","beginner","coding",
        "Implement LIFO stack using two queues.",
        "On push: enqueue to q2. Pour all from q1 to q2. Swap q1 and q2. Pop is just dequeue from q1. Push O(n), Pop O(1). Alt: single queue rotate.",
        ["queue","stack","design"],["Microsoft"])

    # ── Hashing (topic=6) ──

    # Basics (sub=36)
    add(S,6,36,"Two Sum Problem","beginner","coding",
        "Find two numbers that add up to a target. Return indices.",
        "Hashmap: for each num, check if (target - num) exists in map. If yes return indices. Else add num:index to map. O(n) time, O(n) space.",
        ["hashing"],["Amazon","Google"])
    add(S,6,36,"Design a HashSet","intermediate","coding",
        "Design a HashSet without built-in hash functions.",
        "Array of buckets (linked lists). Hash function: key % bucket_size. Add: if not exists, append. Remove: find and delete node. Contains: search bucket. Resize when load factor > threshold.",
        ["hashing","design"],["Amazon"])

    # Frequency (sub=37)
    add(S,6,37,"Top K Frequent Elements","intermediate","coding",
        "Find k most frequent elements in an array.",
        "Counter + heap: count frequencies O(n), heapify or use quickselect for top k O(n log k). Alt: bucket sort by frequency O(n).",
        ["hashing","heap"],["Amazon","Google"])
    add(S,6,37,"First Unique Character","beginner","coding",
        "Find first non-repeating character in a string.",
        "Count frequencies with hashmap. Second pass: return first char with count=1. O(n) time.",
        ["hashing","strings"],["Amazon"])

    # Subarray (sub=38)
    add(S,6,38,"Longest Subarray with Sum K","intermediate","coding",
        "Find length of longest subarray with sum equal to K.",
        "Prefix sum + hashmap: store first occurrence of each prefix sum. If prefix[i]-K exists in map, subarray found. Track max length. O(n).",
        ["hashing","prefix_sum"],["Google"])
    add(S,6,38,"Count Subarrays with Equal 0s and 1s","intermediate","coding",
        "In binary array, find count of subarrays with equal 0s and 1s.",
        "Replace 0 with -1. Problem becomes: count subarrays with sum 0. Use prefix sum + hashmap counting occurrences. O(n).",
        ["hashing","prefix_sum"],["Amazon"])

    # Hashing Advanced (sub=39)
    add(S,6,39,"Longest Consecutive Sequence","intermediate","coding",
        "Find length of longest consecutive elements sequence in unsorted array.",
        "HashSet: for each number, only start counting if num-1 not in set (it's a sequence start). Count forward. O(n) overall.",
        ["hashing"],["Amazon","Google"])
    add(S,6,39,"4Sum Problem","advanced","coding",
        "Find all unique quadruplets that sum to target.",
        "Sort + fix two elements + two pointer for remaining two. Or hashmap: store all pair sums. Check complementary pairs. O(n^3) or O(n^2) with more space.",
        ["hashing","two_pointers"],["Amazon"])

    # ── Recursion (topic=7) ──

    # Basics (sub=40) - has 2
    add(S,7,40,"Power Set","intermediate","coding",
        "Generate all subsets of a given set using recursion.",
        "Include/exclude for each element. Base case: processed all elements, add current subset to result. 2^n subsets. O(n * 2^n) total.",
        ["recursion","backtracking"],["Amazon"])

    # Divide and Conquer (sub=41)
    add(S,7,41,"Merge Sort Implementation","intermediate","coding",
        "Implement merge sort and explain its complexity.",
        "Divide array in half, recursively sort each, merge. Merge: two pointers comparing elements. O(n log n) time (always), O(n) space. Stable sort.",
        ["recursion","sorting"],["Amazon","Google"])
    add(S,7,41,"Count Inversions in Array","advanced","coding",
        "Count pairs where i < j but arr[i] > arr[j], using merge sort.",
        "Modified merge sort: during merge step, when right element chosen before left, count inversions (remaining left elements are all inversions). O(n log n).",
        ["recursion","merge_sort"],["Amazon"])

    # Recursion Advanced (sub=42)
    add(S,7,42,"Tower of Hanoi","intermediate","coding",
        "Solve Tower of Hanoi for n disks. Explain the recursive approach.",
        "Move n-1 disks from source to auxiliary. Move nth disk from source to destination. Move n-1 disks from auxiliary to destination. 2^n - 1 moves. Classic recursion example.",
        ["recursion"],["TCS"])
    add(S,7,42,"Generate All Permutations","intermediate","coding",
        "Generate all permutations of a given array using recursion.",
        "Fix first element, recursively permute rest. Swap approach: for each position, swap with all remaining elements, recurse, swap back. n! permutations.",
        ["recursion","backtracking"],["Amazon"])

    # ── Binary Search (topic=8) ──

    # Basics (sub=43)
    add(S,8,43,"Binary Search Iterative","beginner","coding",
        "Implement binary search iteratively on a sorted array.",
        "left=0, right=n-1. While left<=right: mid=(left+right)//2. If target found return mid. If target>arr[mid] left=mid+1. Else right=mid-1. O(log n).",
        ["binary_search"],["Amazon"])
    add(S,8,43,"First and Last Position","intermediate","coding",
        "Find first and last position of target in sorted array.",
        "Two binary searches: one for leftmost (continue searching left even when found), one for rightmost. O(log n).",
        ["binary_search"],["Amazon","Google"])

    # Bounds (sub=44)
    add(S,8,44,"Lower Bound and Upper Bound","intermediate","coding",
        "Implement lower_bound (first >= target) and upper_bound (first > target).",
        "Lower bound: if arr[mid]>=target, ans=mid, right=mid-1. Upper bound: if arr[mid]>target, ans=mid, right=mid-1. Both O(log n).",
        ["binary_search","bounds"],["Amazon"])
    add(S,8,44,"Count Occurrences in Sorted Array","beginner","coding",
        "Count occurrences of target in sorted array using binary search.",
        "Find first and last position. Count = last - first + 1. If not found return 0. O(log n).",
        ["binary_search","bounds"],["Microsoft"])

    # Search on Answer (sub=45)
    add(S,8,45,"Koko Eating Bananas","intermediate","coding",
        "Find minimum eating speed to finish all banana piles in h hours.",
        "Binary search on answer: search speed from 1 to max(piles). For each speed calculate hours needed. Minimize speed where hours <= h. O(n log max).",
        ["binary_search"],["Google"])
    add(S,8,45,"Allocate Minimum Pages","advanced","coding",
        "Allocate books to students minimizing maximum pages assigned.",
        "Binary search on answer: search from max(pages) to sum(pages). For each mid check if books can be split among k students. O(n log sum).",
        ["binary_search"],["Google","Amazon"])

    # Peak (sub=46)
    add(S,8,46,"Find Peak in Mountain Array","intermediate","coding",
        "Find peak index in a mountain array (increases then decreases).",
        "Binary search: if arr[mid] < arr[mid+1] peak is right, else left. O(log n). Mountain = bitonic array.",
        ["binary_search","peak"],["Amazon"])
    add(S,8,46,"Find Minimum in Rotated Array II","advanced","coding",
        "Find minimum in rotated sorted array with duplicates.",
        "Binary search: if arr[mid] > arr[right] search right. If arr[mid] < arr[right] search left. If equal, right--. O(log n) avg, O(n) worst.",
        ["binary_search","rotation"],["Google"])

    # ── Sorting (topic=9) ──

    # Basic Sorts (sub=47)
    add(S,9,47,"Insertion Sort","beginner","coding",
        "Implement insertion sort and explain when it's preferred.",
        "For each element, insert into correct position in sorted prefix by shifting. O(n^2) worst, O(n) nearly sorted. Stable, in-place. Good for small or nearly sorted arrays.",
        ["sorting"],["TCS"])
    add(S,9,47,"Selection Sort","beginner","coding",
        "Implement selection sort. Why is it O(n^2) even for sorted input?",
        "Find minimum in unsorted portion, swap to front. Always O(n^2) because always scans entire unsorted portion regardless. Unstable, in-place.",
        ["sorting"],["TCS"])

    # Efficient Sorts (sub=48) - has 2
    add(S,9,48,"Quick Sort Partition Schemes","intermediate","coding",
        "Compare Lomuto and Hoare partition schemes in QuickSort.",
        "Lomuto: pivot at end, i tracks boundary. Simpler but more swaps. Hoare: two pointers from both ends, fewer swaps. Both O(n) partition. Quick Sort overall O(n log n) average.",
        ["sorting","quicksort"],["Google"])

    # Non-Comparison (sub=49)
    add(S,9,49,"Counting Sort","beginner","coding",
        "Implement counting sort. When is it preferred over comparison sorts?",
        "Count frequency of each element. Prefix sum of counts. Place elements at correct positions. O(n+k) where k=range. Stable. Better than O(n log n) when range is small.",
        ["sorting"],["Amazon"])
    add(S,9,49,"Radix Sort","intermediate","coding",
        "Implement radix sort. What is its time complexity?",
        "Sort by least significant digit to most, using stable sort (counting sort) at each digit. O(d*(n+k)) where d=digits, k=base. Good for integers and strings.",
        ["sorting"],["Microsoft"])

    # ── Two Pointers (topic=10) ──

    # Basics (sub=50)
    add(S,10,50,"Remove Duplicates from Sorted Array","beginner","coding",
        "Remove duplicates in-place from sorted array. Return new length.",
        "Two pointers: slow for write position, fast for scanning. If fast != slow, increment slow and copy. O(n) time, O(1) space.",
        ["two_pointers"],["Amazon"])
    add(S,10,50,"Pair with Given Sum","beginner","coding",
        "In sorted array find pair with given sum.",
        "Two pointers: left=0, right=n-1. If sum too small, left++. Too large, right--. Equal, found. O(n) time.",
        ["two_pointers"],["TCS"])

    # Intermediate (sub=51)
    add(S,10,51,"Trapping Rain Water Two Pointer","intermediate","coding",
        "Solve trapping rain water using two pointer approach.",
        "Left and right pointers with leftMax and rightMax. Move pointer with smaller max inward. Water at position = max - height. O(n) time, O(1) space.",
        ["two_pointers"],["Amazon","Google"])
    add(S,10,51,"Sort Array by Parity","beginner","coding",
        "Move all even numbers to front and odd to back.",
        "Two pointers: left finds odd, right finds even, swap. Similar to Dutch flag with 2 partitions. O(n).",
        ["two_pointers"],["Amazon"])

    # ── Sliding Window (topic=11) ──

    # Fixed (sub=52)
    add(S,11,52,"Maximum Sum of K Consecutive","beginner","coding",
        "Find maximum sum of k consecutive elements.",
        "Compute first window sum. Slide: add right element, remove left element. Track max. O(n).",
        ["sliding_window"],["Amazon"])
    add(S,11,52,"Average of Subarrays of Size K","beginner","coding",
        "Find average of all contiguous subarrays of size k.",
        "Same as max sum but compute average. Slide window adding right, removing left, divide by k. O(n).",
        ["sliding_window"],["TCS"])

    # Variable (sub=53)
    add(S,11,53,"Smallest Subarray with Sum >= S","intermediate","coding",
        "Find length of smallest subarray with sum >= S.",
        "Variable sliding window: expand right until sum >= S. Shrink left while sum still >= S, track min length. O(n).",
        ["sliding_window"],["Google"])
    add(S,11,53,"Longest Subarray with K Distinct","intermediate","coding",
        "Find longest subarray with at most K distinct characters.",
        "Variable window with hashmap tracking frequencies. When distinct > K, shrink left. Track max length. O(n).",
        ["sliding_window","hashing"],["Amazon"])

    # ── Backtracking (topic=12) ──

    # Basics (sub=54)
    add(S,12,54,"Word Search in Grid","intermediate","coding",
        "Find if a word exists in a grid of characters (adjacent cells).",
        "DFS/backtracking from each cell. Mark visited, explore 4 directions, unmark on backtrack. O(m*n*4^L) where L=word length.",
        ["backtracking","matrix"],["Amazon","Google"])
    add(S,12,54,"Sudoku Solver","advanced","coding",
        "Solve a 9x9 Sudoku puzzle using backtracking.",
        "For each empty cell try 1-9. Check row, column, and 3x3 box constraints. If valid, recurse. If stuck, backtrack. Constraint propagation speeds up.",
        ["backtracking"],["Google"])

    # Permutations (sub=55)
    add(S,12,55,"Permutations with Duplicates","intermediate","coding",
        "Generate all unique permutations of array with duplicate elements.",
        "Sort array first. In backtracking, skip if same element at same position (nums[i]==nums[i-1] and i-1 not used). Avoids duplicate permutations.",
        ["backtracking","permutations"],["Amazon"])
    add(S,12,55,"Next Permutation","intermediate","coding",
        "Find next lexicographically greater permutation of a number array.",
        "From right find first decreasing element i. Find smallest element > nums[i] to its right, swap. Reverse suffix after i. O(n).",
        ["permutations"],["Google"])

    # Subsets (sub=56)
    add(S,12,56,"Subsets II (with duplicates)","intermediate","coding",
        "Generate all unique subsets of array with duplicates.",
        "Sort first. In recursion skip if nums[i]==nums[i-1] at same level (not first choice at this depth). Avoids duplicate subsets.",
        ["backtracking","subsets"],["Amazon"])
    add(S,12,56,"Combination Sum","intermediate","coding",
        "Find all combinations that sum to target. Can reuse elements.",
        "Sort. Backtrack: for each candidate, if <= remaining target include it and recurse with same index (reuse). O(2^target).",
        ["backtracking","subsets"],["Amazon","Google"])

    # N-Queens (sub=57)
    add(S,12,57,"N-Queens Problem","advanced","coding",
        "Place N queens on NxN board such that no two attack each other.",
        "Backtracking row by row. Track occupied columns, diagonals (row-col) and anti-diagonals (row+col). Place queen if all three are free. O(N!).",
        ["backtracking","n_queens"],["Google"])
    add(S,12,57,"Knight's Tour Problem","advanced","coding",
        "Find a path for knight to visit every cell on NxN board exactly once.",
        "Backtracking: from current cell try all 8 moves. Mark visited. If all cells visited, done. Use Warnsdorff's heuristic for efficiency.",
        ["backtracking"],["Amazon"])

    # ── Trees (topic=13) ──

    # Basics (sub=58)
    add(S,13,58,"Height of Binary Tree","beginner","coding",
        "Find the height of a binary tree.",
        "Recursive: height = 1 + max(height(left), height(right)). Base case: null node returns -1 (or 0 depending on definition). O(n).",
        ["trees","recursion"],["Amazon"])
    add(S,13,58,"Count Nodes in Binary Tree","beginner","coding",
        "Count total nodes in a binary tree.",
        "Recursive: count = 1 + count(left) + count(right). Base: null returns 0. For complete binary tree: O(log^2 n) using height comparison.",
        ["trees","recursion"],["TCS"])

    # Traversal (sub=59)
    add(S,13,59,"Level Order Traversal","beginner","coding",
        "Print binary tree level by level using BFS.",
        "Queue-based BFS: enqueue root. While queue not empty, process level (dequeue all at current level, enqueue children). O(n).",
        ["trees","bfs"],["Amazon"])
    add(S,13,59,"Inorder Without Recursion","intermediate","coding",
        "Implement inorder traversal iteratively using a stack.",
        "Stack: push all left children. Pop and process. Move to right child. Repeat. Morris traversal for O(1) space using threaded binary tree.",
        ["trees","stack"],["Amazon"])

    # LCA (sub=60)
    add(S,13,60,"LCA of Binary Tree","intermediate","coding",
        "Find lowest common ancestor of two nodes in a binary tree.",
        "Recursive: if node is null or matches p or q return node. Recurse left and right. If both return non-null, current node is LCA. Else return whichever is non-null. O(n).",
        ["trees","recursion"],["Amazon","Google"])
    add(S,13,60,"LCA of BST","beginner","coding",
        "Find LCA in a BST using BST property.",
        "If both p and q are smaller, go left. Both larger, go right. Otherwise current node is LCA (split point). O(h) time.",
        ["trees","bst"],["Amazon"])

    # Diameter (sub=61)
    add(S,13,61,"Diameter of Binary Tree","intermediate","coding",
        "Find the diameter (longest path between any two nodes) of a binary tree.",
        "DFS: at each node diameter through it = left_height + right_height. Track global max. Return 1 + max(left, right) as height. O(n).",
        ["trees","dfs"],["Amazon","Google"])
    add(S,13,61,"Check if Binary Tree is Balanced","beginner","coding",
        "Check if a binary tree is height-balanced (heights differ by at most 1).",
        "DFS returning height. If abs(left_height - right_height) > 1 at any node, return -1 (unbalanced). O(n) single pass.",
        ["trees","recursion"],["Amazon"])

    # ── BST (topic=14) ──

    # Basics (sub=63)
    add(S,14,63,"Insert into BST","beginner","coding",
        "Insert a value into a Binary Search Tree.",
        "Compare with current node. If smaller go left, if larger go right. When null found, insert. Recursive or iterative. O(h) time.",
        ["bst"],["TCS"])
    add(S,14,63,"Delete from BST","intermediate","coding",
        "Delete a node from BST handling all 3 cases.",
        "Leaf: remove. One child: replace with child. Two children: replace with inorder successor (smallest in right subtree) or predecessor, then delete successor. O(h).",
        ["bst"],["Amazon"])

    # Validation (sub=64)
    add(S,14,64,"Validate BST","intermediate","coding",
        "Check if a binary tree is a valid BST.",
        "Recursive: pass min/max range. Each node must be within (min, max). Left child: update max=node.val. Right child: update min=node.val. O(n). Alt: inorder should be sorted.",
        ["bst","validation"],["Amazon","Google"])
    add(S,14,64,"Recover BST","advanced","coding",
        "Two nodes in BST are swapped. Recover the tree.",
        "Inorder traversal: find two violations (first where prev > curr, second where prev > curr). Swap those two nodes. O(n) time, O(1) space with Morris.",
        ["bst"],["Amazon"])

    # Kth Smallest (sub=65)
    add(S,14,65,"Kth Smallest in BST","intermediate","coding",
        "Find kth smallest element in a BST.",
        "Inorder traversal (gives sorted order). Count k elements. Stop at kth. O(h+k). Alt: augmented BST with subtree sizes for O(h).",
        ["bst","inorder"],["Amazon","Google"])
    add(S,14,65,"Kth Largest in BST","intermediate","coding",
        "Find kth largest element in a BST.",
        "Reverse inorder (right, root, left). Count k elements. O(h+k). Or find (n-k+1)th smallest.",
        ["bst","inorder"],["Amazon"])

    # ── Heaps (topic=15) ──

    # Basics (sub=66)
    add(S,15,66,"Build Max Heap","beginner","coding",
        "Build a max heap from an unsorted array.",
        "Heapify from last non-leaf node to root. siftDown at each. O(n) build time (not O(n log n)). Parent of i: (i-1)//2. Children: 2i+1, 2i+2.",
        ["heap"],["TCS"])
    add(S,15,66,"Heap Sort","intermediate","coding",
        "Implement heap sort using a max heap.",
        "Build max heap O(n). Extract max n times: swap root with last, reduce size, siftDown. O(n log n). Not stable, in-place.",
        ["heap","sorting"],["Amazon"])

    # Top K (sub=67)
    add(S,15,67,"Kth Largest Element","intermediate","coding",
        "Find kth largest element using a min-heap of size k.",
        "Maintain min-heap of k elements. For each new element, if > heap min, replace. Heap root is kth largest. O(n log k).",
        ["heap"],["Amazon","Google"])
    add(S,15,67,"Top K Frequent Words","intermediate","coding",
        "Find k most frequent words, sorted by frequency then alphabetically.",
        "Count frequencies. Min-heap of size k with custom comparator. Or bucket sort by frequency. O(n log k).",
        ["heap","hashing"],["Amazon"])

    # Median (sub=68)
    add(S,15,68,"Find Median in Data Stream","advanced","coding",
        "Design structure to find median from a stream of numbers.",
        "Two heaps: max-heap for lower half, min-heap for upper half. Balance sizes (differ by at most 1). Median from tops. O(log n) insert, O(1) median.",
        ["heap","design"],["Amazon","Google"])
    add(S,15,68,"Sliding Window Median","expert","coding",
        "Find median of each sliding window of size k.",
        "Two heaps (like stream median) with lazy deletion via hashmap. Or sorted list with bisect. O(n log k). Complex rebalancing on window slide.",
        ["heap","sliding_window"],["Google"])

    # ── Graphs (topic=16) ──

    # Basics (sub=69)
    add(S,16,69,"Graph Representations","beginner","conceptual",
        "Compare adjacency matrix and adjacency list representations.",
        "Adjacency Matrix: O(V^2) space, O(1) edge lookup, good for dense graphs. Adjacency List: O(V+E) space, O(degree) edge lookup, good for sparse graphs. Most real-world graphs are sparse, prefer list.",
        ["graphs"],["TCS"])
    add(S,16,69,"Connected Components","intermediate","coding",
        "Find number of connected components in an undirected graph.",
        "BFS/DFS from each unvisited node. Each traversal marks one component. Count traversals. Or Union-Find: union edges, count distinct roots. O(V+E).",
        ["graphs","union_find"],["Amazon"])

    # BFS (sub=70)
    add(S,16,70,"Shortest Path in Unweighted Graph","intermediate","coding",
        "Find shortest path from source to all nodes in unweighted graph.",
        "BFS from source. Distance array: dist[neighbor] = dist[current] + 1. BFS guarantees shortest path in unweighted graphs. O(V+E).",
        ["graphs","bfs"],["Amazon"])
    add(S,16,70,"Rotting Oranges","intermediate","coding",
        "Find minimum time for all oranges to rot (multi-source BFS).",
        "Add all rotten oranges to queue (multi-source). BFS level by level. Each level = 1 minute. If fresh remain after BFS, return -1. O(m*n).",
        ["graphs","bfs","matrix"],["Amazon","Google"])

    # DFS (sub=71)
    add(S,16,71,"Number of Islands","intermediate","coding",
        "Count islands in a grid (connected 1s surrounded by 0s).",
        "DFS/BFS from each unvisited '1'. Mark all connected as visited. Count starts. O(m*n).",
        ["graphs","dfs","matrix"],["Amazon","Google"])
    add(S,16,71,"Path Exists in Graph","beginner","coding",
        "Check if path exists between two nodes.",
        "DFS/BFS from source. If destination reached return true. Or Union-Find: check if same component. O(V+E).",
        ["graphs","dfs"],["Amazon"])

    # Cycle Detection (sub=72)
    add(S,16,72,"Detect Cycle in Directed Graph","intermediate","coding",
        "Detect if a directed graph contains a cycle.",
        "DFS with 3 colors: white (unvisited), gray (in stack), black (done). Back edge (to gray node) = cycle. Or Kahn's algorithm: if topological sort doesn't include all nodes, cycle exists. O(V+E).",
        ["graphs","cycle"],["Amazon","Google"])
    add(S,16,72,"Detect Cycle in Undirected Graph","intermediate","coding",
        "Detect cycle in undirected graph.",
        "DFS: if neighbor is visited and not parent, cycle exists. Or Union-Find: if two nodes of an edge are already in same set, cycle. O(V+E).",
        ["graphs","cycle","union_find"],["Amazon"])

    # Topological Sort (sub=73)
    add(S,16,73,"Course Schedule","intermediate","coding",
        "Given course prerequisites, determine if all courses can be finished.",
        "Topological sort using Kahn's (BFS with indegree) or DFS. If all nodes processed, no cycle. Else impossible. O(V+E).",
        ["graphs","topological_sort"],["Amazon","Google"])
    add(S,16,73,"Task Scheduling Order","intermediate","coding",
        "Find valid task execution order given dependencies.",
        "Topological sort: Kahn's algorithm. Queue nodes with indegree 0. Process, decrement neighbors' indegree. If any becomes 0, add to queue. Result is valid order.",
        ["graphs","topological_sort"],["Amazon"])

    # MST (sub=75)
    add(S,16,75,"Kruskal's Algorithm","advanced","coding",
        "Find MST using Kruskal's algorithm.",
        "Sort edges by weight. For each edge, if connecting different components (Union-Find), add to MST. Stop when V-1 edges. O(E log E).",
        ["graphs","mst","union_find"],["Amazon"])
    add(S,16,75,"Prim's Algorithm","advanced","coding",
        "Find MST using Prim's algorithm.",
        "Start from any node. Min-heap of edges. Add cheapest edge to unvisited node. Mark visited. Repeat until all visited. O(E log V). Better for dense graphs.",
        ["graphs","mst","heap"],["Google"])

    # ── Greedy (topic=17) ──

    # Basics (sub=76)
    add(S,17,76,"Fractional Knapsack","beginner","coding",
        "Solve fractional knapsack using greedy approach.",
        "Sort by value/weight ratio descending. Take items greedily. If item doesn't fit fully, take fraction. Greedy works because fractions allowed. O(n log n).",
        ["greedy"],["TCS"])
    add(S,17,76,"Assign Cookies","beginner","coding",
        "Maximize content children given cookie sizes and child greed factors.",
        "Sort both. Greedily assign smallest sufficient cookie to least greedy child. Two pointers. O(n log n).",
        ["greedy","two_pointers"],["Amazon"])

    # Activity Selection (sub=77)
    add(S,17,77,"Non-Overlapping Intervals","intermediate","coding",
        "Find minimum intervals to remove for non-overlapping set.",
        "Sort by end time. Greedily keep intervals that don't overlap with last kept. Remove count = total - kept. O(n log n).",
        ["greedy","intervals"],["Amazon","Google"])
    add(S,17,77,"Job Sequencing Problem","intermediate","coding",
        "Schedule jobs with deadlines to maximize profit.",
        "Sort by profit descending. For each job, assign to latest available slot before deadline. Union-Find for efficient slot finding. O(n log n).",
        ["greedy"],["Amazon"])

    # Greedy Advanced (sub=78)
    add(S,17,78,"Huffman Coding","advanced","coding",
        "Build Huffman tree for optimal prefix-free encoding.",
        "Min-heap: take two smallest freq nodes, create parent with sum. Repeat until one node. Tree gives variable-length codes. Greedy: combine least frequent first. O(n log n).",
        ["greedy","heap","trees"],["Google"])
    add(S,17,78,"Minimum Platforms","intermediate","coding",
        "Find minimum platforms needed at a railway station.",
        "Sort arrivals and departures separately. Two pointers: merge-like comparison. When arrival <= departure, need platform. Else free one. Track max. O(n log n).",
        ["greedy","sorting"],["Amazon"])

    # ── Dynamic Programming (topic=18) ──

    # Basics (sub=79)
    add(S,18,79,"Climbing Stairs","beginner","coding",
        "Find number of ways to climb n stairs (1 or 2 steps at a time).",
        "dp[i] = dp[i-1] + dp[i-2]. Fibonacci! Base: dp[0]=1, dp[1]=1. Space optimize to two variables. O(n) time, O(1) space.",
        ["dp"],["Amazon"])
    add(S,18,79,"Coin Change","intermediate","coding",
        "Find minimum coins to make amount. Return -1 if impossible.",
        "dp[amount] = min(dp[amount-coin]+1) for all coins. Base: dp[0]=0. Init: infinity. O(amount * coins). Classic unbounded knapsack.",
        ["dp"],["Amazon","Google"])

    # 1D DP (sub=80)
    add(S,18,80,"House Robber","intermediate","coding",
        "Maximum money robbing non-adjacent houses.",
        "dp[i] = max(dp[i-1], dp[i-2]+nums[i]). Skip or rob current. O(n) time, O(1) space with two variables.",
        ["dp"],["Amazon"])
    add(S,18,80,"Decode Ways","intermediate","coding",
        "Count ways to decode a digit string (1=A, 26=Z).",
        "dp[i] = dp[i-1] (if valid single digit) + dp[i-2] (if valid two digits 10-26). O(n).",
        ["dp","strings"],["Amazon","Google"])

    # Knapsack (sub=81)
    add(S,18,81,"0/1 Knapsack","intermediate","coding",
        "Solve 0/1 knapsack: maximize value within weight capacity.",
        "2D DP: dp[i][w] = max(dp[i-1][w], dp[i-1][w-weight[i]]+value[i]). Take or skip item. Space optimize to 1D (iterate weight backward). O(n*W).",
        ["dp","knapsack"],["Amazon"])
    add(S,18,81,"Partition Equal Subset Sum","intermediate","coding",
        "Can array be partitioned into two subsets with equal sum?",
        "Total sum must be even. Reduce to: can we find subset with sum = total/2? This is 0/1 knapsack. dp[j] = dp[j] || dp[j-nums[i]]. O(n*sum).",
        ["dp","knapsack"],["Amazon"])

    # LIS (sub=82)
    add(S,18,82,"Longest Increasing Subsequence","intermediate","coding",
        "Find length of LIS in an array.",
        "O(n^2): dp[i] = max(dp[j]+1) for all j < i where nums[j] < nums[i]. O(n log n): patience sort with binary search on tails array.",
        ["dp","binary_search"],["Amazon","Google"])
    add(S,18,82,"Russian Doll Envelopes","advanced","coding",
        "Max envelopes you can put inside each other (width AND height must be strictly larger).",
        "Sort by width ascending. For same width sort by height descending. Find LIS on heights. O(n log n).",
        ["dp","LIS"],["Google"])

    # LCS (sub=83)
    add(S,18,83,"Longest Common Subsequence","intermediate","coding",
        "Find LCS of two strings.",
        "2D DP: if chars match dp[i][j]=dp[i-1][j-1]+1. Else dp[i][j]=max(dp[i-1][j],dp[i][j-1]). Backtrack for actual subsequence. O(m*n).",
        ["dp","strings"],["Amazon"])
    add(S,18,83,"Shortest Common Supersequence","advanced","coding",
        "Find shortest string that has both s1 and s2 as subsequences.",
        "Find LCS first. Build result by merging both strings following LCS. Length = m+n-LCS_length. O(m*n).",
        ["dp","strings"],["Google"])

    # ── Tries (topic=19) ──

    # Basics (sub=85)
    add(S,19,85,"Implement Trie","intermediate","coding",
        "Implement a Trie with insert, search, and startsWith methods.",
        "TrieNode: children dict + is_end flag. Insert: create nodes along path. Search: follow path, check is_end. StartsWith: follow path, return true if exists. O(word_length) for all ops.",
        ["trie"],["Amazon","Google"])
    add(S,19,85,"Word Search II","advanced","coding",
        "Find all words from dictionary in a grid using Trie.",
        "Build Trie from dictionary. DFS from each cell, follow Trie. Prune: if no Trie path, stop. Much faster than checking each word separately. O(m*n*4^L).",
        ["trie","backtracking","matrix"],["Google"])

    # Autocomplete (sub=86)
    add(S,19,86,"Autocomplete System","advanced","coding",
        "Design autocomplete: given prefix, return top 3 suggestions by frequency.",
        "Trie where each node stores list of (sentence, frequency). On input character, traverse Trie, return top 3. Update frequency on sentence completion. O(prefix_length + results).",
        ["trie","design"],["Google","Amazon"])
    add(S,19,86,"Spell Checker Using Trie","intermediate","coding",
        "Implement a spell checker that suggests corrections for misspelled words.",
        "Build Trie of dictionary. For misspelled word: BFS/DFS with edit distance 1-2 (insert, delete, replace characters at each position). Return matches from Trie.",
        ["trie","strings"],["Google"])

    # ── Union Find (topic=20) ──

    # Basics (sub=87)
    add(S,20,87,"Union-Find Implementation","intermediate","coding",
        "Implement Union-Find with path compression and union by rank.",
        "find(x): if parent[x]!=x, parent[x]=find(parent[x]). Path compression: flattens tree. union(x,y): attach smaller rank tree under larger. Near O(1) amortized (inverse Ackermann).",
        ["union_find"],["Amazon","Google"])
    add(S,20,87,"Number of Provinces","intermediate","coding",
        "Find number of connected components using Union-Find.",
        "For each edge union the two nodes. Count distinct roots (find(i)==i). Same as connected components via DFS but Union-Find is more efficient for dynamic connectivity.",
        ["union_find","graphs"],["Amazon"])

    # ── Additional Expert Questions ──

    add(S,1,11,"Median of Two Sorted Arrays","expert","coding",
        "Find median of two sorted arrays in O(log(min(m,n))).",
        "Binary search on smaller array partition. Ensure left partition elements <= right partition elements in both arrays. Partition at i in arr1 and (m+n+1)/2-i in arr2. O(log min(m,n)).",
        ["binary_search","arrays"],["Google","Amazon"])

    add(S,18,84,"Word Break Problem","expert","coding",
        "Determine if string can be segmented into dictionary words.",
        "DP: dp[i] = true if s[:i] can be segmented. For each i check all j < i: dp[j] and s[j:i] in dict. O(n^2 * m). Trie optimization possible.",
        ["dp","strings","trie"],["Amazon","Google"])

    add(S,18,84,"Matrix Chain Multiplication","expert","coding",
        "Find minimum multiplications to multiply chain of matrices.",
        "Interval DP: dp[i][j] = min cost to multiply matrices i..j. Try all split points k: dp[i][k] + dp[k+1][j] + p[i-1]*p[k]*p[j]. O(n^3).",
        ["dp","interval_dp"],["Amazon"])

    add(S,16,74,"Network Delay Time","expert","coding",
        "Find time for signal to reach all nodes in weighted directed graph.",
        "Dijkstra from source. Answer = max distance to any reachable node. If any unreachable return -1. O((V+E) log V).",
        ["graphs","dijkstra"],["Google"])

    add(S,13,62,"Morris Inorder Traversal","expert","coding",
        "Implement O(1) space inorder traversal without stack or recursion.",
        "Threaded binary tree: if no left child process node, go right. If left child: find inorder predecessor. If predecessor.right is null, set to current, go left. If predecessor.right is current, remove thread, process, go right. O(n) time, O(1) space.",
        ["trees","morris"],["Google"])

    add(S,3,27,"Design TTL Cache with LRU Eviction","expert","coding",
        "Design cache supporting both TTL expiry and LRU eviction policy.",
        "Combine LRU (doubly linked list + hashmap) with TTL (expiry timestamp per entry). On get: check TTL, evict if expired. Background thread or lazy expiry. Priority queue for TTL ordering. O(1) amortized ops.",
        ["lru_cache","design"],["Amazon","Uber"])

    add(S,16,69,"Strongly Connected Components","expert","coding",
        "Find all SCCs in a directed graph using Kosaraju's algorithm.",
        "Two passes: (1) DFS on original graph, push to stack by finish time. (2) DFS on transpose graph in stack order. Each DFS tree is an SCC. O(V+E). Alt: Tarjan's with single DFS.",
        ["graphs","dfs"],["Google"])

    add(S,6,38,"Maximum Length Subarray Sum Zero","expert","coding",
        "Find longest subarray with sum equal to zero.",
        "Prefix sum + hashmap. Store first occurrence of each prefix sum. If same prefix sum appears again, subarray between them has sum 0. Track max length. O(n).",
        ["hashing","prefix_sum"],["Amazon"])

    add(S,11,53,"Minimum Window Containing All Elements","expert","coding",
        "Find smallest window containing all elements of a given set.",
        "Variable sliding window with hashmap. Expand right until all elements covered. Shrink left while still covered. Track minimum window. O(n).",
        ["sliding_window","hashing"],["Google","Amazon"])

    add(S,12,54,"Rat in a Maze All Paths","expert","coding",
        "Find all paths from top-left to bottom-right in a maze.",
        "Backtracking: try all 4 directions from current cell. Mark visited, recurse, unmark. Collect all paths reaching destination. Exponential worst case.",
        ["backtracking","matrix"],["Amazon"])

    conn.commit()

    cur.execute('SELECT COUNT(*) FROM questions')
    total = cur.fetchone()[0]
    print(f"Inserted {count} new questions. Total: {total}")

    cur.execute('SELECT difficulty, COUNT(*) FROM questions GROUP BY difficulty ORDER BY difficulty')
    print("\nDifficulty distribution:")
    for r in cur.fetchall():
        print(f"  {r[0]}: {r[1]}")

    cur.execute('''
        SELECT s.name, COUNT(q.id)
        FROM subjects s LEFT JOIN questions q ON q.subject_id = s.id
        GROUP BY s.name ORDER BY s.name
    ''')
    print("\nSubject totals:")
    for r in cur.fetchall():
        print(f"  {r[0]}: {r[1]}")

    # Check remaining thin subtopics
    cur.execute('''
        SELECT COUNT(*) FROM (
            SELECT sub.id FROM subtopics sub
            LEFT JOIN questions q ON q.subtopic_id = sub.id
            GROUP BY sub.id HAVING COUNT(q.id) < 3
        ) t
    ''')
    print(f"\nSubtopics still < 3 questions: {cur.fetchone()[0]}")

    conn.close()

if __name__ == "__main__":
    run()
