# Design an LRU Cache with TTL Expiration

**Difficulty:** Hard  
**Topics:** Cache Design, LRU Eviction, TTL Expiration, Data Structures

## Problem Statement

Design and implement a fixed-capacity **Least Recently Used (LRU) Cache with Time-to-Live (TTL)** expiration.

The cache stores key-value pairs. Each entry may have an expiration deadline, after which it must no longer be accessible.

The cache supports four operations:

1. `put` — Insert or update a key-value pair.
2. `get` — Retrieve a value and update its recency.
3. `delete` — Explicitly remove a key.
4. `size` — Return the number of currently valid entries.

Before processing **every operation**, the cache must remove all entries whose expiration deadlines are less than or equal to the operation timestamp.

If inserting a new key would exceed the cache capacity, evict the least recently used valid entry.

Return exactly one result for every operation, preserving the original operation order.

## Function Signatures

Implement the following Python classes and functions:

```python
class Cache:
    def __init__(self, capacity: int):
        pass

    def put(self, key: str, value: int,
            ttl: int, ts: int) -> None:
        pass

    def get(self, key: str, ts: int) -> int | None:
        pass

    def delete(self, key: str, ts: int) -> bool:
        pass

    def size(self, ts: int) -> int:
        pass


def run_cache(
    operations: list[list],
    capacity: int
) -> list:
    pass
```

The `run_cache` function initializes a cache and executes each operation in sequence.

## Operation Formats

Each operation is represented by an array whose second element is its timestamp.

| Operation | Input format | Return value |
|---|---|---|
| Put | `["put", ts, key, value, ttl]` | `None` |
| Get | `["get", ts, key]` | Value or `None` |
| Delete | `["delete", ts, key]` | `True` or `False` |
| Size | `["size", ts]` | Integer |

## Detailed Requirements

### 1. TTL Expiration

Every `put` operation specifies a TTL.

- If `ttl > 0`, the expiration deadline is `ts + ttl`.
- If `ttl == 0`, the entry never expires.
- An entry expires when `current_time >= expiration_deadline`.
- Expired entries must be removed before processing any operation.
- Reading an entry does not extend its TTL.
- Updating an existing key replaces its TTL and resets its expiration deadline.

For example:

```python
put("a", 10, ttl=5, ts=0)
```

The key is valid at timestamps 0 through 4 and expires at timestamp 5.

### 2. LRU Eviction

The cache has a maximum capacity.

When a new key is inserted and the cache is full, evict the least recently used valid key.

Recency is updated when:

- A key is successfully retrieved using `get`.
- A key is inserted using `put`.
- An existing key is updated using `put`.

Unsuccessful `get` operations do not change recency.

Expiration cleanup does not refresh the recency of other entries.

### 3. Updating Existing Keys

When `put` is called for an existing key:

- Replace its stored value.
- Replace its TTL and expiration deadline.
- Mark it as the most recently used entry.
- Do not increase the number of entries.
- Do not evict another entry merely because an existing key is updated.

### 4. Explicit Deletion

`delete(key, ts)` removes the specified key if it currently exists.

- Return `True` if the key was successfully removed.
- Return `False` if the key does not exist or has already expired.
- Deletion immediately frees cache capacity.

### 5. Size

`size(ts)` returns the number of non-expired entries currently stored in the cache.

Expired entries must be removed before calculating the size.

## Examples

### Example 1: TTL Expiration and LRU Eviction

**Input**

```python
operations = [
    ["put", 0, "a", 10, 5],
    ["put", 1, "b", 20, 0],
    ["get", 2, "a"],
    ["put", 3, "c", 30, 0],
    ["get", 4, "b"],
    ["get", 5, "a"],
    ["size", 5]
]

capacity = 2
```

**Output**

```python
[None, None, 10, None, None, None, 1]
```

**Explanation**

- At time 0, `a` is inserted and expires at time 5.
- At time 1, `b` is inserted without expiration.
- At time 2, accessing `a` makes it most recently used.
- At time 3, inserting `c` evicts `b`, the least recently used entry.
- At time 4, `b` is absent.
- At time 5, `a` expires.
- The cache contains only `c`, so its size is 1.

### Example 2: Updating an Existing Key

**Input**

```python
operations = [
    ["put", 0, "a", 100, 5],
    ["put", 2, "a", 200, 10],
    ["get", 5, "a"],
    ["get", 12, "a"],
    ["size", 12]
]

capacity = 2
```

**Output**

```python
[None, None, 200, None, 0]
```

**Explanation**

Updating `a` at time 2 replaces its value and moves its expiration deadline to time 12. It remains valid at time 5 but expires at time 12.

### Example 3: Explicit Deletion

**Input**

```python
operations = [
    ["put", 0, "a", 10, 0],
    ["delete", 1, "a"],
    ["delete", 2, "a"],
    ["get", 3, "a"],
    ["size", 4]
]

capacity = 2
```

**Output**

```python
[None, True, False, None, 0]
```

## Constraints and Assumptions

- `capacity >= 1`.
- Operation timestamps are nonnegative and nondecreasing.
- Multiple operations may have the same timestamp.
- TTL values are nonnegative integers.
- Keys are strings and values are integers.
- Operations are executed sequentially in the given order.
- No concurrency is required in the base problem.

## Interview Follow-ups

After implementing the basic cache, discuss:

1. What is the time complexity of `get`, `put`, `delete`, and `size`?
2. Can expired entries be identified without scanning the entire cache?
3. How should expiration be handled when an existing key's TTL changes?
4. What happens when multiple expiration records exist for the same key?
5. How can stale expiration records be handled efficiently?
6. Can expiration tracking consume significantly more memory than the cache itself?
7. How would you bound expiration-tracking memory?
8. How would you analyze the amortized complexity of periodic cleanup?
9. How would you make the cache thread-safe?
10. How could you improve concurrency without a single global lock?

**Goal:** Build a correct cache, maintain TTL and LRU semantics, and explain the performance and memory trade-offs of your implementation.
