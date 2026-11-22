# Coding Interview: LRU Cache with TTL and Lazy Expiration

**Difficulty:** Hard  
**Topics:** HashMap, Doubly Linked List, Min-Heap, Lazy Deletion, Amortized Analysis

## Problem Statement

Design and implement a fixed-capacity **Least Recently Used (LRU) Cache with Time-To-Live (TTL)** expiration.

The cache must support the following operations:

- `put(key, value, ttl, current_time)` — Insert or update a key with a specified TTL.
- `get(key, current_time)` — Return the value if the key exists and has not expired; otherwise return `-1`.

### Requirements

1. The cache has a fixed capacity of `N` entries.
2. Each entry has an expiration deadline calculated as `current_time + ttl`.
3. An entry is expired when `current_time >= expiration_deadline`.
4. Before each operation, remove all expired entries.
5. A successful `get()` updates the key's LRU recency.
6. Every `put()` updates the key's LRU recency.
7. If the cache is full when inserting a new key, evict the least recently used non-expired entry.
8. Updating an existing key replaces its value and expiration deadline.
9. Return exactly one result per operation, using `-1` for cache misses and a specified acknowledgment (such as `null`) for puts.

**Assumptions:** Operation timestamps are nondecreasing, TTL values are positive, and the cache is single-threaded unless otherwise specified.

---

## Interview Follow-up Questions

### Follow-up 1: Basic TTL Expiration

**Interviewer:**

Your cache contains 1 million entries, each with a different expiration deadline.

Before processing every operation, you must remove expired entries.

How would you implement expiration cleanup?

**Discussion questions:**

- Would scanning the entire hashmap work?
- What is its time complexity?
- Can we identify expired entries without scanning all N entries?
- If only K entries have expired, can cleanup be faster than O(N)?

### Follow-up 2: Efficient Expiration Tracking

**Interviewer:**

Suppose the cache contains 1 million entries, but only 2 have expired.

Can you design a data structure that efficiently identifies the earliest expiration deadline?

**Discussion questions:**

- What data structure would you use?
- How efficiently can you access the earliest expiration?
- What is the complexity of removing K expired records?
- What additional data must be stored alongside each deadline?

### Follow-up 3: Updating TTL

**Interviewer:**

Consider the following operations:

```python
put("A", 100, ttl=10, current_time=0)
put("A", 200, ttl=30, current_time=2)
```

The first expiration deadline is 10, and the updated deadline is 32.

Suppose your expiration data structure contains both records.

At time 10, how do you prevent the old expiration record from incorrectly deleting A?

**Discussion questions:**

- How do you distinguish an outdated expiration record from a current one?
- Should you update or remove the old record immediately?
- What happens when the same key is updated multiple times?
- Would comparing deadlines alone always be sufficient?

### Follow-up 4: Lazy Deletion

**Interviewer:**

Removing an arbitrary element from a standard min-heap can require linear time.

Can we avoid immediately removing outdated expiration records when a key is updated?

**Discussion questions:**

- What is lazy deletion?
- When should outdated records actually be removed?
- How do you verify whether a heap record is still valid?
- What happens if the hashmap no longer contains the key?
- Why should an outdated record be discarded rather than reinserted?

### Follow-up 5: Duplicate Heap Records

**Interviewer:**

Suppose the heap contains:

```python
[(10, "A"), (30, "A")]
```

But the hashmap contains:

```python
{"A": (200, 30)}
```

At time 10, you discover that the first heap record is outdated.

Should you reinsert `(30, "A")` into the heap?

**Discussion questions:**

- What happens if you reinsert it?
- Is it acceptable to have multiple heap records for the same key?
- How can you identify which record represents the current version?
- How would you handle a key that is evicted and later reinserted with the same expiration deadline?

### Follow-up 6: Unbounded Heap Growth

**Interviewer:**

Your cache capacity is only 100 entries.

However, one key is updated 1 million times before its expiration records are processed.

Your hashmap contains at most 100 entries, but your heap may contain 1 million records.

Would you consider this acceptable for a production cache?

**Discussion questions:**

- Why can lazy deletion cause unbounded memory growth?
- How would you prevent the heap from growing indefinitely?
- Can you reduce memory consumption without sacrificing efficient updates?
- What trade-offs would your approach introduce?

### Follow-up 7: Heap Compaction

**Interviewer:**

Suppose you decide to periodically rebuild the heap using only the current valid cache entries.

For a cache with capacity 100, imagine rebuilding when the heap exceeds 200 records.

**Discussion questions:**

- How would you rebuild the heap?
- What is the time complexity of rebuilding?
- How would you choose a compaction threshold?
- What happens if the cache contains only 2 live entries but has capacity for 1 million?
- Can the heap size be bounded by O(N), where N is the cache capacity?

### Follow-up 8: Amortized Complexity

**Interviewer:**

Heap rebuilding takes O(N), which is more expensive than a normal heap insertion.

How can you argue that periodic heap rebuilding still provides efficient performance over many cache operations?

**Discussion questions:**

- What is the difference between worst-case and amortized complexity?
- If rebuilding costs O(N) but happens once every O(N) updates, what is the amortized rebuilding cost per update?
- Can the overall update operation remain O(log N) amortized?
- Does this guarantee that every individual operation completes in O(log N)?
- How would you justify your compaction policy formally?

### Follow-up 9: Integrating LRU with TTL

**Interviewer:**

Now combine TTL expiration with LRU eviction.

Suppose the cache is full and a new key is inserted.

Some entries have expired, while others remain valid.

**Discussion questions:**

- In what order should expiration cleanup and LRU eviction occur?
- Should an expired entry count toward cache capacity?
- Does reading an expired key update its recency?
- How do you keep the LRU structure and expiration tracking consistent?
- What happens to expiration records when a key is evicted due to capacity?

### Follow-up 10: Production-Level Design

**Interviewer:**

Your implementation works correctly in a single-threaded environment.

Now imagine it is used by a high-throughput, multithreaded service.

**Discussion questions:**

- What race conditions could occur between `get()`, `put()`, expiration cleanup, and LRU eviction?
- Would a single global lock be sufficient?
- How could you improve concurrency?
- What changes if multiple threads update the same key's TTL?
- How would you handle heap compaction without blocking all cache operations for too long?

---

## Final Interview Challenge

Implement the cache and explain:

1. Your chosen data structures and why each is necessary.
2. How `get()` and `put()` work.
3. How expiration cleanup works.
4. How stale heap entries are detected.
5. How duplicate expiration records are handled.
6. How heap memory growth is controlled.
7. How LRU eviction interacts with TTL expiration.
8. Worst-case and amortized time complexity.
9. Space complexity.
10. Edge cases and concurrency considerations.

**Interviewer expectation:** Prioritize correctness first, then efficient expiration handling, bounded memory usage, and a clear explanation of amortized complexity.

Do not assume every operation must have O(1) worst-case complexity. Explain the trade-offs of the chosen design.
