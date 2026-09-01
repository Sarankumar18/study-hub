# LC #1482 — Minimum Number of Days to Make m Bouquets — Complete Guide

> Date: 2026-08-25 | Pattern: Binary Search on Answer Space | Difficulty: Medium | LC#: 1482  
> NeetCode: [minimum-number-of-days-to-make-m-bouquets](https://neetcode.io/solutions/minimum-number-of-days-to-make-m-bouquets)

---

## Problem

You are given:

- `bloomDay[i]` — day on which flower `i` blooms
- `m` — number of bouquets needed
- `k` — each bouquet needs **k adjacent** flowers

Return the **minimum number of days** you must wait to make `m` bouquets.  
If impossible, return `-1`.

```text
Input:  bloomDay = [1,10,3,10,2], m = 3, k = 1
Output: 3

By day 3: flowers at indices 0,2,4 have bloomed → 3 bouquets of size 1
```

```text
Input:  bloomDay = [7,7,7,7,12,7,7], m = 2, k = 3
Output: 12

Need 2 groups of 3 adjacent bloomed flowers.
By day 12: [7,7,7,7,12,7,7] all bloomed → indices 0-2 and 4-6 work
```

---

## Pattern

**Binary Search on Answer Space (Template 4)** — same family as LC #875 and LC #1011.

You are NOT searching an array index. You are searching for the **minimum day `d`** such that:

```text
feasible(d) = true   →  we can make m bouquets by day d
```

Monotonic property:

```text
If day d works, any day > d also works (more flowers bloomed).
If day d fails, any day < d also fails.

false false false true true true
                  ↑
            first valid day
```

---

## Approach 1: Brute Force

### Idea

Try every possible day from `min(bloomDay)` to `max(bloomDay)`. Return the first day where `m` bouquets are possible.

### Pseudocode

```text
if n < m * k:
    return -1

for day from min(bloomDay) to max(bloomDay):
    if canMakeBouquets(bloomDay, day, m, k):
        return day

return -1

function canMakeBouquets(bloomDay, day, m, k):
    bouquets = 0
    consecutive = 0
    for each bloom in bloomDay:
        if bloom <= day:
            consecutive++
            if consecutive == k:
                bouquets++
                consecutive = 0
        else:
            consecutive = 0
    return bouquets >= m
```

### Complexity

- Time: O((max - min) × n) — try each day, scan array each time
- Space: O(1)

### Why it is not enough

`max(bloomDay)` can be up to 10^9. Linear scan over days is too slow.

---

## Approach 2: Optimal — Binary Search on Days

### Idea

Binary search on the answer range `[left, right]` where:

```text
left  = min(bloomDay)
right = max(bloomDay)
```

For each candidate `mid` (days to wait), run `canMakeBouquets(mid)`.

```text
if feasible(mid):
    right = mid      // mid works, try fewer days
else:
    left = mid + 1   // need more days
```

### Pseudocode

```text
if n < m * k:
    return -1

left = min(bloomDay)
right = max(bloomDay)

while left < right:
    mid = left + (right - left) / 2
    if canMakeBouquets(bloomDay, mid, m, k):
        right = mid
    else:
        left = mid + 1

return canMakeBouquets(bloomDay, left, m, k) ? left : -1
```

### Trace

```text
bloomDay = [7,7,7,7,12,7,7], m = 2, k = 3

Impossible check: n=7 >= 6 ✅

left=7, right=12

mid=9:  bloomDay[4]=12 > 9 → streak breaks at index 4
        Only one group of 3 at indices 0-2 → bouquets=1 < 2 → fail
        left = 10

mid=11: index 4 still not bloomed → still 1 bouquet → fail
        left = 12

left=12, right=12 → loop ends

canMake(12): all bloom → two groups [0-2] and [4-6] → 2 bouquets ✅
return 12
```

### Complexity

- Time: O(n log(max - min)) — log range × O(n) feasibility per step
- Space: O(1)

---

## Java Implementation

```java
class Solution {
    public int minDays(int[] bloomDay, int m, int k) {
        int n = bloomDay.length;
        if ((long) m * k > n) {
            return -1;
        }

        int left = Integer.MAX_VALUE;
        int right = Integer.MIN_VALUE;
        for (int day : bloomDay) {
            left = Math.min(left, day);
            right = Math.max(right, day);
        }

        while (left < right) {
            int mid = left + (right - left) / 2;
            if (canMake(bloomDay, mid, m, k)) {
                right = mid;
            } else {
                left = mid + 1;
            }
        }

        return canMake(bloomDay, left, m, k) ? left : -1;
    }

    private boolean canMake(int[] bloomDay, int days, int m, int k) {
        int bouquets = 0;
        int consecutive = 0;

        for (int bloom : bloomDay) {
            if (bloom <= days) {
                consecutive++;
                if (consecutive == k) {
                    bouquets++;
                    consecutive = 0;
                }
            } else {
                consecutive = 0;
            }
        }

        return bouquets >= m;
    }
}
```

---

## Java Internals

### `(long) m * k > n` guard

```java
if (m * k > n)  // can OVERFLOW when m and k are large
```

`m` and `k` can be up to 10^5 each. Product exceeds `Integer.MAX_VALUE`. Cast to `long` before multiply.

### Why reset `consecutive = 0` after making a bouquet

Adjacent means non-overlapping groups in a left-to-right scan:

```text
k=2, bloomDay = [1,1,1,1]
Day 1: [1,1] bouquet → indices 0-1 used
       next bouquet starts at index 2, not index 1
```

After `consecutive == k`, reset to 0 (not `k-1` overlap). Each flower used in at most one bouquet in this greedy scan.

### No collections needed

Pure `int[]` scan. No `HashMap`, no sorting. O(1) extra space.

---

## Edge Cases

| Case | Handling |
|------|----------|
| `m * k > n` | Impossible — return `-1` |
| `k == 1` | Each flower is its own bouquet — find m-th smallest bloom day (BS still works) |
| All same bloom day | `left == right` quickly |
| Single element, m=1, k=1 | Return `bloomDay[0]` |
| Large bloom days (10^9) | BS on range, not brute force days |

---

## Common Mistakes

1. **Forgetting adjacency** — counting any k flowers instead of k **consecutive**
2. **`m * k` overflow** — use `(long) m * k`
3. **`right = mid - 1`** when finding minimum — use `right = mid`
4. **Not resetting consecutive on bloom > days** — streak must break
5. **Overlapping bouquets** — reset consecutive to 0 after each bouquet, not k-1

---

## Compare to LC #875 and #1011

| Problem | Answer (mid) | `feasible(mid)` |
|---------|--------------|-----------------|
| LC #875 Koko | eating speed | total hours ≤ h |
| LC #1011 Ship | ship capacity | days needed ≤ days |
| LC #1482 Bouquets | days to wait | bouquets made ≥ m (adjacent k) |

Same template. Only `canMake()` / `feasible()` changes.

---

## 60-Second Interview Explanation

> This is binary search on the answer — the minimum day to wait. The answer lies between the minimum and maximum bloom day. For a candidate day, I scan the array left to right: if a flower has bloomed by that day, I extend a consecutive counter; when it reaches k, I form one bouquet and reset. If the bloom day exceeds the candidate, I reset the streak. If total bouquets is at least m, the day is feasible. Because waiting longer only helps, feasibility is monotonic — binary search finds the minimum valid day in O(n log(max-min)) time and O(1) space.

---

## Practice Exercise

```text
bloomDay = [1,10,2,9,3,8,4,7,5,6], m = 4, k = 2

1. Is it possible? (check m*k vs n)
2. What are left and right?
3. For mid = 5, how many bouquets can you make? Trace the scan.
```

<details>
<summary>Answer</summary>

n=10, m*k=8 → possible.

left=1, right=10.

mid=5: bloomed indices where bloomDay<=5: [1,2,3,5,5] at indices 0,2,4,6,8
Scan: 1→streak1, 2→streak2→bouquet1, 3→streak1, 5→streak2→bouquet2, 5→streak1
Only 2 bouquets at day 5. Need 4 → not feasible.

</details>
