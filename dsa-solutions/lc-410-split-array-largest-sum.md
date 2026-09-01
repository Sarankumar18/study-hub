# LC #410 — Split Array Largest Sum — Complete Guide

> Date: 2026-08-28 | Pattern: Binary Search on Answer Space | Difficulty: Hard | LC#: 410  
> NeetCode: [split-array-largest-sum](https://neetcode.io/solutions/split-array-largest-sum)

---

## Problem

Given integer array `nums` and integer `k`, split `nums` into **exactly `k` non-empty contiguous subarrays**. Minimize the **largest subarray sum** among all valid splits.

```text
Input:  nums = [7, 2, 5, 10, 8], k = 2
Output: 18

Split: [7, 2, 5] | [10, 8]  →  max(14, 18) = 18
```

---

## Pattern

**Binary Search on Answer Space (Template 4)** — same family as LC #875, #1011, #1482.

Search the **minimum** value `X` such that:

```text
feasible(X) = true   →  array can be split into k parts with each part sum ≤ X
```

Monotonic:

```text
false false false true true true
                  ↑
         minimum valid max subarray sum
```

---

## Approach 1: Brute Force

### Idea

Try every possible way to place `k-1` split points. Track the maximum subarray sum for each split. Return the minimum of those maxima.

### Pseudocode

```text
best = infinity
for each combination of k-1 split positions:
    compute max subarray sum for that split
    best = min(best, that max)

return best
```

### Complexity

- Time: O(C(n-1, k-1) * n) — exponential in splits
- Space: O(k)

### Why it fails

`n` up to 1000, `k` up to 50 — combinatorial explosion.

---

## Approach 2: DP

### Idea

`dp[i][j]` = minimum possible largest sum when splitting first `i` elements into `j` parts.

### Pseudocode

```text
for i from 1 to n:
    for j from 1 to k:
        dp[i][j] = infinity
        for p from j-1 to i-1:
            left = max sum in nums[0..p]
            dp[i][j] = min(dp[i][j], max(dp[p][j-1], left))
```

### Complexity

- Time: O(n² * k)
- Space: O(n * k)

### Why BS is better

O(n log S) where S = sum(nums) — typically faster and cleaner to explain in interviews.

---

## Approach 3: Optimal — BS on Answer + Greedy Feasibility

### Key insight

The answer lies between `max(nums)` and `sum(nums)`.

For candidate `mid`, ask: **what is the minimum number of parts** needed if no part may exceed `mid`?

Greedy packing (same spirit as Ship Packages):

```text
parts = 1
currentSum = 0
for num in nums:
    if currentSum + num > mid:
        parts++
        currentSum = num
    else:
        currentSum += num
return parts <= k
```

**Why `parts <= k`?**

- Greedy gives **minimum** parts forced by limit `mid`.
- If `parts < k`, split any part further → still ≤ `mid`.
- If `parts > k`, even best packing fails → `mid` too small.

### Complexity

- Time: O(n log(sum(nums)))
- Space: O(1)

---

## Java Implementation

```java
class Solution {
    public int splitArray(int[] nums, int k) {
        int left = 0;
        int right = 0;

        for (int num : nums) {
            left = Math.max(left, num);
            right += num;
        }

        while (left < right) {
            int mid = left + (right - left) / 2;
            if (canSplit(nums, k, mid)) {
                right = mid;
            } else {
                left = mid + 1;
            }
        }
        return left;
    }

    private boolean canSplit(int[] nums, int k, int maxSum) {
        int parts = 1;
        int current = 0;

        for (int num : nums) {
            if (current + num > maxSum) {
                parts++;
                current = num;
            } else {
                current += num;
            }
        }
        return parts <= k;
    }
}
```

---

## Java Internals

- **`int` sums:** For LC constraints (`nums[i] <= 10^6`, `n <= 1000`), `sum(nums)` fits in `int` (~10^9). No `long` needed unless constraints grow.
- **Enhanced for-loop:** `for (int num : nums)` avoids index bounds mistakes in the greedy pass.
- **No collections:** Pure primitives — zero allocation in hot path; good for interview performance discussion.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `left = 0` | `left = max(nums)` — answer never below largest element |
| `parts >= k` in feasibility | Use `parts <= k` — greedy counts **minimum** parts needed |
| `parts == k` | Too strict when greedy uses fewer parts than `k` |
| `currentSum = 0` after split | Set `currentSum = num` — new part must include current element |
| Confusing with #1011 direction | Ship: `days <= D`; here: `parts <= k` |

---

## Edge Cases

```text
nums = [1], k = 1           → 1
nums = [1,2,3,4], k = 1     → 10
nums = [1,2,3,4], k = 4     → 4
nums = [10,5], k = 2        → 10
```

---

## 60-Second Interview Explanation

> "I'm minimizing the largest subarray sum, and that value is monotonic — if `mid` works, any larger limit works too. So I binary search between `max(nums)` and `sum(nums)`. For each `mid`, I greedily pack elements into subarrays without exceeding `mid` and count how many parts I need. If that's at most `k`, `mid` is feasible and I try smaller; otherwise I go larger. The greedy count is the minimum parts required, which is why the check is `parts <= k`."

---

## Practice Exercise

Trace `nums = [7,2,5,10,8]`, `k = 2`, `mid = 18`:

1. How many parts does greedy produce?
2. Is `mid = 17` feasible? Why?

<details>
<summary>Answers</summary>

1. Parts = 2: [7,2,5]=14, then [10,8]=18.
2. No. [7,2,5]=14, then 10 alone, then 8 alone → 3 parts > 2.

</details>
