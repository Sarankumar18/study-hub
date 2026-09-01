# Binary Search — Complete Study Guide

> **Phase 1, Pattern #4** | 10 problems | You: **5/10 solved** (LC #33, #153, #162, #875, #1011)
> **Read this fully before solving the remaining 5 problems.**

---

## Table of Contents

1. [Description](#1-description)
2. [Applications](#2-applications)
3. [Types & Variants](#3-types--variants)
4. [Templates (Pseudocode)](#4-templates-pseudocode)
5. [Operations & Loop Invariants](#5-operations--loop-invariants)
6. [Java Implementation Notes](#6-java-implementation-notes)
7. [Complexity Summary](#7-complexity-summary)
8. [Recognition Signals](#8-recognition-signals)
9. [Common Mistakes](#9-common-mistakes)
10. [Your Progress & Problem Order](#10-your-progress--problem-order)

---

## 1. Description

**Binary Search** is a divide-and-conquer technique that repeatedly **cuts the search space in half** by comparing the middle element (or middle candidate answer) against a condition.

```text
Sorted:  [1, 3, 5, 7, 9, 11, 13]
          L        M           R

Step 1: compare target with nums[M]
        → go left or right
        → discard half the array

Repeat until found or space is empty.
```

### Core requirement

Binary search works when the search space has a **monotonic property**:

```text
false false false true true true true
              ↑
         first true (boundary)

OR

valid valid valid invalid invalid
                  ↑
            last valid (boundary)
```

If you can say "everything to the left is X, everything to the right is Y", you can binary search.

### Two search spaces

| Search space | What you binary search ON |
|--------------|---------------------------|
| **Index space** | Indices in a sorted array (0 … n-1) |
| **Answer space** | Possible values of the answer (1 … max) |

Most beginners only know index-space BS. **Interviews love answer-space BS** (Koko, Ship Packages, Split Array).

---

## 2. Applications

### In interviews

| Use case | Example problems |
|----------|------------------|
| Find element in sorted data | LC #34, #378 |
| Find boundary / insertion point | LC #34 (first/last position) |
| Rotated sorted array | LC #33, #153 |
| Find peak / local maximum | LC #162 |
| Minimize maximum / maximize minimum | LC #875, #1011, #1482, #410 |
| Median of sorted structures | LC #4 |
| Kth element in structured matrix | LC #378 |

### In real systems (backend relevance)

| System | Binary search role |
|--------|-------------------|
| **Database indexes** | B-tree lookup is repeated binary search on pages |
| **Load balancing** | Consistent hashing ring — find successor node |
| **Time-series storage** | Find timestamp bucket in sorted segments |
| **Git bisect** | Find first bad commit (answer-space BS) |
| **Rate limiter config** | Find minimum threshold that satisfies SLA |

---

## 3. Types & Variants

Binary Search is one pattern with **6 variants**. Know which variant a problem uses.

```text
                    BINARY SEARCH
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   On Index          On Answer       On Structure
        │                │                │
   ┌────┴────┐      ┌────┴────┐     ┌────┴────┐
   │         │      │         │     │         │
 Standard  Rotated  Minimize  Peak  Matrix   Median
 Search    Array    Answer    Find  Search   of 2
 (#34)     (#33)    (#875)   (#162) (#378)  (#4)
```

### Variant map

| # | Variant | Question shape | Loop style | Your status |
|---|---------|----------------|------------|-------------|
| A | **Standard search** | Find target in sorted array | `left <= right` | — |
| B | **Rotated sorted** | Sorted array rotated at pivot | `left <= right` | ✅ LC #33 |
| C | **Find min in rotated** | Find rotation point / minimum | `left < right`, `right = mid` | ✅ LC #153 |
| D | **Peak finding** | Any peak where `nums[i] > neighbors` | `left < right`, `right = mid` | ✅ LC #162 |
| E | **Binary search on answer** | Min speed / min capacity / min days | `left < right`, `right = mid` | ✅ LC #875, #1011 |
| F | **First / last position** | Sorted array with duplicates | Two passes, biased mid | ⬜ LC #34 |
| G | **Matrix / 2D** | Row-sorted or fully sorted matrix | BS on rows + BS on cols | ⬜ LC #378 |
| H | **Median of two arrays** | Two sorted arrays, find median | Partition shorter array | ⬜ LC #4 |

---

## 4. Templates (Pseudocode)

### Template 1 — Standard search (`left <= right`)

**Use when:** exact match in sorted array. Return index or -1.

```text
left = 0
right = n - 1

while left <= right:
    mid = left + (right - left) / 2

    if nums[mid] == target:
        return mid
    else if nums[mid] < target:
        left = mid + 1
    else:
        right = mid - 1

return -1
```

**Invariant:** if target exists, it is always in `[left, right]`.

---

### Template 2 — Rotated sorted array search

**Use when:** array was sorted, then rotated. LC #33.

```text
left = 0
right = n - 1

while left <= right:
    mid = left + (right - left) / 2

    if nums[mid] == target:
        return mid

    if nums[left] <= nums[mid]:
        // left half is sorted
        if target >= nums[left] and target < nums[mid]:
            right = mid - 1
        else:
            left = mid + 1
    else:
        // right half is sorted
        if target > nums[mid] and target <= nums[right]:
            left = mid + 1
        else:
            right = mid - 1

return -1
```

**Key insight:** one half is ALWAYS sorted. Check if target fits in the sorted half.

**Your solved problems:** LC #33 ✅

---

### Template 3 — Find minimum (`left < right`, `right = mid`)

**Use when:** find smallest value satisfying a property, or min in rotated array. LC #153, #162, #875, #1011.

```text
left = 0
right = n - 1   // or left = minAnswer, right = maxAnswer

while left < right:
    mid = left + (right - left) / 2

    if condition(mid) is on the RIGHT side:
        left = mid + 1
    else:
        right = mid       // mid might be the answer — do NOT do mid - 1

return left   // or nums[left] for rotated min
```

**Rotated min (LC #153):**

```text
while left < right:
    mid = left + (right - left) / 2
    if nums[mid] > nums[right]:
        left = mid + 1      // min is in right half
    else:
        right = mid         // min is in left half including mid
return nums[left]
```

**Peak element (LC #162):**

```text
while left < right:
    mid = left + (right - left) / 2
    if nums[mid] < nums[mid + 1]:
        left = mid + 1      // peak is to the right
    else:
        right = mid         // peak is at mid or to the left
return left
```

**Your solved problems:** LC #153 ✅, LC #162 ✅

---

### Template 4 — Binary search on answer space

**Use when:** "find minimum X such that feasible(X) is true". LC #875, #1011, #1482, #410.

```text
left = minimum possible answer
right = maximum possible answer

while left < right:
    mid = left + (right - left) / 2

    if feasible(mid):
        right = mid         // mid works, try smaller
    else:
        left = mid + 1      // mid too small, need bigger

return left
```

**Feasibility function changes per problem:**

| Problem | Answer (mid) | `feasible(mid)` checks |
|---------|--------------|------------------------|
| LC #875 Koko | eating speed | total hours at speed `mid` <= h |
| LC #1011 Ship | ship capacity | days needed at capacity `mid` <= days |
| LC #1482 Bouquets | days to wait | can make m bouquets in `mid` days |
| LC #410 Split Array | max subarray sum | can split into k parts with max sum `mid` |

**Your solved problems:** LC #875 ✅, LC #1011 ✅

**Ceiling division trick (Java integers):**

```text
ceil(pile / speed) = (pile + speed - 1) / speed
```

Why `-1`? Adds just enough to round up only when there is a remainder, without affecting exact divisions.

---

### Template 5 — First / last position (biased binary search)

**Use when:** sorted array with duplicates. LC #34.

**Find FIRST occurrence:**

```text
left = 0, right = n - 1, result = -1

while left <= right:
    mid = left + (right - left) / 2
    if nums[mid] == target:
        result = mid
        right = mid - 1     // keep searching left for earlier occurrence
    else if nums[mid] < target:
        left = mid + 1
    else:
        right = mid - 1

return result
```

**Find LAST occurrence:** same but `left = mid + 1` when found.

Run **two separate binary searches**. One pass cannot give both bounds reliably.

---

### Template 6 — Kth smallest in sorted matrix (LC #378)

**Use when:** each row sorted, first element of row > last element of previous row.

```text
// Binary search on VALUE, not index
left = matrix[0][0]
right = matrix[n-1][n-1]

while left < right:
    mid = left + (right - left) / 2
    count = countElementsLessOrEqual(matrix, mid)

    if count < k:
        left = mid + 1
    else:
        right = mid

return left
```

`countElementsLessOrEqual` walks each row from right to left — O(n) per check.

---

### Template 7 — Median of two sorted arrays (LC #4) — Hard

**Idea:** binary search on partition position in the **shorter** array.

```text
if nums1.length > nums2.length:
    swap(nums1, nums2)

m = len(nums1), n = len(nums2)
half = (m + n + 1) / 2

left = 0, right = m

while left <= right:
    partition1 = (left + right) / 2
    partition2 = half - partition1

    maxLeft1  = partition1 == 0 ? MIN : nums1[partition1 - 1]
    minRight1 = partition1 == m   ? MAX : nums1[partition1]
    maxLeft2  = partition2 == 0 ? MIN : nums2[partition2 - 1]
    minRight2 = partition2 == n   ? MAX : nums2[partition2]

    if maxLeft1 <= minRight2 and maxLeft2 <= minRight1:
        // correct partition found
        if (m + n) is odd:
            return max(maxLeft1, maxLeft2)
        else:
            return (max(maxLeft1, maxLeft2) + min(minRight1, minRight2)) / 2
    else if maxLeft1 > minRight2:
        right = partition1 - 1
    else:
        left = partition1 + 1
```

Draw the partition line on paper. This is Google's favorite Hard — study after finishing the other 9.

---

## 5. Operations & Loop Invariants

### The three loop styles

| Style | Loop | On success | On fail | Returns | Used for |
|-------|------|------------|---------|---------|----------|
| **Exact match** | `left <= right` | `return mid` | shrink both sides | index or -1 | Standard, rotated search |
| **Find minimum valid** | `left < right` | `right = mid` | `left = mid + 1` | `left` | Answer space, min in rotated, peak |
| **Find maximum valid** | `left < right` | `left = mid + 1` | `right = mid` | `left` | "Maximize minimum" problems |

### Mid calculation — always use this

```java
int mid = left + (right - left) / 2;
```

```text
(left + right) / 2          → integer OVERFLOW when left + right > 2^31 - 1
left + (right - left) / 2   → always safe
```

### Decision flowchart

```text
Is the problem asking for a VALUE in a sorted array?
  YES → Template 1 or 2 or 5

Is it asking for MINIMUM of something that can be too small or too big?
  YES → Template 4 (answer space)

Is it asking for a rotation point, peak, or boundary?
  YES → Template 3 (left < right, right = mid)

Is it a 2D matrix or two arrays?
  YES → Template 6 or 7
```

---

## 6. Java Implementation Notes

### Primitive types and overflow

```java
// BAD — hours can overflow int when speed = 1 and piles are large
int totalHours = 0;

// GOOD
long totalHours = 0;
for (int pile : piles) {
    totalHours += (pile + mid - 1L) / mid;
}
```

Use `long` for accumulated sums/products in feasibility checks.

### No special Java collection needed

Binary search is pure index arithmetic on `int[]`. You do not need `TreeMap` or `Collections.binarySearch()` for interview problems.

`Arrays.binarySearch(arr, key)` exists but:
- Returns `-(insertionPoint) - 1` on miss (confusing)
- Does not handle rotated arrays or answer space
- **Implement manually in interviews** to show understanding

### `Arrays.binarySearch` vs manual

| | `Arrays.binarySearch` | Manual BS |
|---|----------------------|-----------|
| Standard sorted array | ✅ Quick | ✅ Preferred in interviews |
| Rotated array | ❌ | ✅ |
| Answer space | ❌ | ✅ |
| First/last position | ❌ (needs wrapper) | ✅ |

---

## 7. Complexity Summary

| Variant | Time | Space | Notes |
|---------|------|-------|-------|
| Standard BS | O(log n) | O(1) | n = array length |
| Rotated / peak | O(log n) | O(1) | Same |
| BS on answer | O(n log R) | O(1) | R = answer range; O(n) feasibility per step |
| First/last position | O(log n) | O(1) | Two passes = still O(log n) |
| Kth in matrix | O(n log(max-min)) | O(1) | n rows, count step is O(n) |
| Median of 2 arrays | O(log(min(m,n))) | O(1) | Partition on shorter array |

### Space

All iterative binary search variants: **O(1) space**. Recursive BS is O(log n) stack — avoid in interviews.

---

## 8. Recognition Signals

```text
✅ "Sorted array" + find / search / position
✅ "Rotated sorted array"
✅ "Find peak element"
✅ "Minimum speed / capacity / days to achieve X"
✅ "Split array into k parts, minimize largest sum"
✅ "Kth smallest" in matrix with sorted rows
✅ "Median of two sorted arrays"
✅ Answer is in a RANGE [min, max] and feasibility is monotonic
```

### NOT binary search

```text
❌ Unsorted array with no structure
❌ Need all pairs / all subarrays (use sliding window or two pointers)
❌ Graph traversal (use BFS/DFS)
❌ "Count ways" / overlapping subproblems (use DP)
```

---

## 9. Common Mistakes

| Mistake | Fix |
|---------|-----|
| `(left + right) / 2` overflow | Use `left + (right - left) / 2` |
| `right = mid - 1` when finding minimum | Use `right = mid` — mid could BE the answer |
| `left <= right` when finding minimum valid | Use `left < right` |
| Wrong boundary in rotated search | Left sorted: `target < nums[mid]` (strict). Right sorted: `target <= nums[right]` |
| Forgetting `nums[left] <= nums[mid]` (not `<`) | When `left == mid`, one-element half must count as sorted |
| `int` overflow in feasibility sum | Use `long` |
| Returning `nums[mid]` after loop | Return `nums[left]` or `left` — mid is stale |
| One BS pass for first AND last position | Run two separate searches |

---

## 10. Your Progress & Problem Order

### Solved — review these with the templates above

| # | Problem | LC# | Variant | Template | Confidence |
|---|---------|-----|---------|----------|------------|
| 21 | Search in Rotated Sorted Array | 33 | Rotated | T2 | Say pattern out loud |
| 22 | Find Min in Rotated Sorted Array | 153 | Min boundary | T3 | `right = mid` |
| 23 | Find Peak Element | 162 | Peak | T3 | Compare mid vs mid+1 |
| 24 | Koko Eating Bananas | 875 | Answer space | T4 | `ceil` trick |
| 25 | Capacity to Ship Packages | 1011 | Answer space | T4 | `left = max(weights)` |

### Remaining — solve in this order

| Order | # | Problem | LC# | Variant | Why this order |
|-------|---|---------|-----|---------|----------------|
| 1 | 26 | Min Days to Make m Bouquets | 1482 | Answer space | Same as #875/#1011 — third practice |
| 2 | 28 | Find First and Last Position | 34 | First/last | New variant (biased BS) |
| 3 | 30 | Kth Smallest in Sorted Matrix | 378 | Matrix value BS | Medium, builds on T4 |
| 4 | 27 | Split Array Largest Sum | 410 | Answer space | Harder feasibility |
| 5 | 29 | Median of Two Sorted Arrays | 4 | Partition BS | Hard capstone — do last |

### Study checklist before each remaining problem

```text
[ ] Which variant? (A–H)
[ ] Which template? (T1–T7)
[ ] Which loop style? (<= vs <, mid vs mid-1)
[ ] What is feasible(mid) or the comparison?
[ ] Edge case: empty, single element, all same
```

---

## Quick Reference Card

```text
┌─────────────────────────────────────────────────────────┐
│  BINARY SEARCH CHEAT SHEET                              │
├─────────────────────────────────────────────────────────┤
│  mid = left + (right - left) / 2                        │
│                                                         │
│  Exact match:     while (left <= right)                │
│  Find minimum:    while (left < right)  right = mid     │
│  Find maximum:    while (left < right)  left = mid + 1  │
│                                                         │
│  ceil(a/b) = (a + b - 1) / b                           │
│                                                         │
│  Rotated: one half always sorted → check target in it   │
│  Answer:  binary search on [minAns, maxAns] + feasible  │
│  Peak:    nums[mid] < nums[mid+1] → go right            │
└─────────────────────────────────────────────────────────┘
```

---

**Next step:** Read sections 3–5 carefully. Map your 5 solved problems to their template numbers. Then solve **LC #1482** (same pattern as Koko/Ship — 15 min if you internalized Template 4).
