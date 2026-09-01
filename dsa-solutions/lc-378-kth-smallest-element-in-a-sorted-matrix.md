# LC #378 — Kth Smallest Element in a Sorted Matrix — Complete Guide

> Date: 2026-08-27 | Pattern: Binary Search on Value | Difficulty: Medium | LC#: 378  
> NeetCode: [kth-smallest-element-in-a-sorted-matrix](https://neetcode.io/solutions/kth-smallest-element-in-a-sorted-matrix)

---

## Problem

Given an `n × n` matrix where:

- Each row is sorted left to right
- The first element of each row is greater than the last element of the previous row

Return the **kth smallest** element (1-indexed).

```text
matrix = [[1,5,9],[10,11,13],[12,13,15]], k = 8
Output: 13
```

Sorted order if flattened: `1,5,9,10,11,12,13,13,15` → 8th = 13

---

## Pattern

**Binary Search on VALUE** (Template 6) — not on index, not on row/col.

Search the answer in range `[matrix[0][0], matrix[n-1][n-1]]`.

For each candidate `mid`, ask: **how many elements are ≤ mid?**

```text
if count >= k  → mid might be answer, try smaller (right = mid)
if count < k   → need bigger value (left = mid + 1)
```

Monotonic: if value `v` has count ≥ k, any larger value also has count ≥ k.

---

## Approach 1: Brute Force

### Idea

Flatten all `n²` elements, sort, return `list[k-1]`.

### Pseudocode

```text
list = []
for each row in matrix:
    for each val in row:
        list.add(val)
sort(list)
return list[k - 1]
```

### Complexity

- Time: O(n² log n²) = O(n² log n)
- Space: O(n²)

### Why it is not enough

Works on LeetCode. Interviewers want O(n log range) with O(1) space.

---

## Approach 2: Better — Min-Heap

### Idea

Each row is sorted. Push `(matrix[i][0], i, 0)` for all rows. Poll k times; after each poll, push next element from same row.

### Pseudocode

```text
heap = min-heap of (value, row, col)
for i in 0..n-1:
    heap.push(matrix[i][0], i, 0)

repeat k times:
    (val, r, c) = heap.pop()
    answer = val
    if c + 1 < n:
        heap.push(matrix[r][c+1], r, c+1)

return answer
```

### Complexity

- Time: O(k log n)
- Space: O(n)

### When to use

Good when **k is small**. When k ≈ n², heap loses to BS on value.

---

## Approach 3: Optimal — Binary Search on Value

### Idea

Binary search on `left = matrix[0][0]` to `right = matrix[n-1][n-1]`.

`countLessOrEqual(matrix, mid)` counts elements ≤ mid in **O(n)** using sorted rows.

### Pseudocode — count function

```text
function countLessOrEqual(matrix, value):
    n = matrix.length
    count = 0
    j = n - 1                    // column pointer, shared across rows

    for i from 0 to n-1:
        while j >= 0 and matrix[i][j] > value:
            j--
        count += j + 1           // elements in row i at cols 0..j are <= value

    return count
```

**Why O(n)?** `j` only moves left across all rows — at most `n` steps total per count.

### Pseudocode — binary search

```text
left = matrix[0][0]
right = matrix[n-1][n-1]

while left < right:
    mid = left + (right - left) / 2
    count = countLessOrEqual(matrix, mid)

    if count >= k:
        right = mid
    else:
        left = mid + 1

return left
```

### Trace

```text
matrix = [[1,5,9],[10,11,13],[12,13,15]], k = 8

BS range [1, 15]:
  mid=8  → count<=8: row0→2, row1→0, row2→0 = 2 < 8 → left=9
  mid=12 → count<=12: 2+2+1 = 5 < 8 → left=13
  mid=13 → count<=13: 2+3+3 = 8 >= 8 → right=13
  left=13 → return 13
```

### Complexity

- Time: O(n log(max - min))
- Space: O(1)

---

## Java Implementation

```java
class Solution {
    public int kthSmallest(int[][] matrix, int k) {
        int n = matrix.length;
        int left = matrix[0][0];
        int right = matrix[n - 1][n - 1];

        while (left < right) {
            int mid = left + (right - left) / 2;
            int count = countLessOrEqual(matrix, mid);

            if (count >= k) {
                right = mid;
            } else {
                left = mid + 1;
            }
        }

        return left;
    }

    private int countLessOrEqual(int[][] matrix, int value) {
        int n = matrix.length;
        int count = 0;
        int j = n - 1;

        for (int i = 0; i < n; i++) {
            while (j >= 0 && matrix[i][j] > value) {
                j--;
            }
            count += j + 1;
        }

        return count;
    }
}
```

---

## Java Internals

- Use `int` for `left`, `right`, `mid` — matrix values fit in int per constraints.
- `left + (right - left) / 2` avoids overflow if bounds are large.
- No collections needed — pure array indexing.
- Return `left` (the value), not an index — kth smallest **value** may appear multiple times.

---

## Edge Cases

| Case | Notes |
|------|-------|
| k = 1 | Return `matrix[0][0]` |
| k = n² | Return `matrix[n-1][n-1]` |
| Duplicate values | Count uses `<=`, correct for kth smallest value |
| n = 1 | Single cell matrix |

---

## Common Mistakes

1. **Binary searching on index** instead of value
2. **O(n²) count** — visiting every cell each BS step
3. **`j` reset per row** — should persist and only move left (shared pointer)
4. **`count > k` vs `count >= k`** — use `>=` for minimum valid value
5. **Returning index** instead of the value at `left`

---

## 60-Second Interview Explanation

> The matrix is row-sorted and each row's start beats the previous row's end, so values are globally ordered but not stored flat. I binary search on the value range from min to max. For each candidate, I count elements less than or equal to it by scanning each row from right to left with a shared column pointer — O(n) per count. If at least k elements are ≤ mid, mid could be the answer so I search lower; otherwise I search higher. Total O(n log(max-min)) time and O(1) space.

---

## Practice Exercise

```text
matrix = [[1,3,5],[6,7,12],[11,14,14]], k = 4

1. What are left and right?
2. For mid = 7, what is countLessOrEqual?
3. What is the answer?
```

<details>
<summary>Answer</summary>

left=1, right=14. mid=7: row0→3 (1,3,5), row1→2 (6,7), row2→1 (11? no 11>7, j stops) → count=3+2+0=5? Let me recalc.

j=2: row0: 5>7? no, 3>7? no, 1>7? no → j stays 2, count += 3
row1: 12>7 j=1, 7>7? no → count += 2 → total 5
row2: 14>7, 11>7 → j=0, 11>7 → j=-1 → count += 0
count=5 >= 4 → search lower...

Answer k=4: sorted 1,3,5,6,... → 4th is 6.

</details>
