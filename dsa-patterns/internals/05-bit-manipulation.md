# Bit Manipulation — Complete Study Guide

> **Phase 1, Pattern #5** | 4 problems | You: **0/4 solved**
> **Read this fully before solving any Bit Manipulation problems.**

---

## Table of Contents

1. [Description](#1-description)
2. [Applications](#2-applications)
3. [Types & Variants](#3-types--variants)
4. [Templates (Pseudocode)](#4-templates-pseudocode)
5. [Operations & Bit Invariants](#5-operations--bit-invariants)
6. [Java Implementation Notes](#6-java-implementation-notes)
7. [Complexity Summary](#7-complexity-summary)
8. [Recognition Signals](#8-recognition-signals)
9. [Common Mistakes](#9-common-mistakes)
10. [Your Progress & Problem Order](#10-your-progress--problem-order)

---

## 1. Description

**Bit manipulation** means reading and changing individual bits in an integer using bitwise operators.

Every `int` in Java is 32 bits (two's complement for negatives):

```text
  5 in binary:  00000000 00000000 00000000 00000101
 13 in binary:  00000000 00000000 00000000 00001101

  5 & 13:       00000000 00000000 00000000 00000101  →  5
  5 | 13:       00000000 00000000 00000000 00001101  →  13
  5 ^ 13:       00000000 00000000 00000000 00001000  →  8
 ~5:            11111111 11111111 11111111 11111010  →  -6 (two's complement)
```

### Core idea

Many interview problems reduce to:

1. **Cancel pairs** with XOR (`a ^ a = 0`)
2. **Count or remove set bits** with `n & (n - 1)`
3. **Build answers from smaller sub-answers** using bit structure (`i >> 1`, `i & 1`)
4. **Simulate arithmetic** with XOR (sum) + AND (carry)

You rarely need to manipulate all 32 bits manually — recognize which **trick** applies.

---

## 2. Applications

### In interviews

| Use case | Example problems |
|----------|------------------|
| Find unique element (others appear twice) | LC #136 |
| Count set bits / hamming weight | LC #191 |
| DP using bit structure | LC #338 |
| Add without `+` / `-` | LC #371 |
| Power of 2 check | `n > 0 && (n & (n-1)) == 0` |
| Subset generation / masks | (later: backtracking) |

### In real systems (backend relevance)

| System | Bit manipulation role |
|--------|----------------------|
| **Permissions / ACLs** | One `int` or `long` = many boolean flags (`READ \| WRITE`) |
| **Bloom filters** | Multiple hash functions set bits in a bit array |
| **Connection pooling flags** | Compact state in a single word |
| **Kafka / protocol headers** | Packed fields in binary formats |
| **Feature flags** | Bitmask toggles per tenant |

Bit manipulation is a **small pattern** (4 problems in Phase 1) — master the 4 tricks, don't over-invest.

---

## 3. Types & Variants

```text
                    BIT MANIPULATION
                           │
     ┌─────────────────────┼─────────────────────┐
     │                     │                     │
  XOR tricks           Bit counting          Bit DP / simulate
  (cancel pairs)       (Kernighan)           (build / add)
     │                     │                     │
  LC #136              LC #191                 LC #338, #371
```

| Variant | When | Key operation |
|---------|------|---------------|
| **A — XOR cancellation** | Every element appears twice except one | `result ^= num` |
| **B — Count set bits** | How many 1-bits in `n`? | `n &= n - 1` in a loop |
| **C — Bit DP** | Answer for `0..n` depends on smaller numbers | `dp[i] = dp[i>>1] + (i&1)` |
| **D — Bitwise addition** | Add without `+` | XOR sum + AND carry, shift carry |
| **E — Masks & flags** | Toggle / test / set bit `k` | `n \| (1<<k)`, `n & ~(1<<k)`, `n & (1<<k)` |
| **F — Power of 2** | Is `n` a power of 2? | `n > 0 && (n & (n-1)) == 0` |

---

## 4. Templates (Pseudocode)

### Template 1 — XOR find single unique (LC #136)

```text
result = 0
for each num in nums:
    result = result XOR num
return result
```

**Why it works:** XOR is commutative and associative. Pairs cancel: `a ^ a = 0`. Odd-count element remains.

---

### Template 2 — Brian Kernighan count bits (LC #191)

```text
count = 0
while n != 0:
    n = n AND (n - 1)    // removes lowest set bit
    count++
return count
```

**Alternative (check each bit):**

```text
count = 0
while n != 0:
    count += n AND 1
    n = n >> 1           // unsigned shift in Java: >>>
return count
```

Kernighan runs in **O(number of set bits)**, not O(32) worst case per call.

---

### Template 3 — Bit DP for 0..n (LC #338)

```text
dp[0] = 0
for i from 1 to n:
    dp[i] = dp[i >> 1] + (i AND 1)

// i >> 1  = i without its last bit (i / 2)
// i & 1   = last bit (0 or 1)
```

**Example:** `i = 13` → binary `1101` → `dp[13] = dp[6] + 1` because `6 = 110` has one fewer bit than `13`.

---

### Template 4 — Add two integers without + (LC #371)

```text
while carry != 0:
    sum = a XOR b           // sum without carry
    carry = (a AND b) << 1  // positions where both had 1
    a = sum
    b = carry
return a
```

**Trace:** `a=5 (101)`, `b=3 (011)`

```text
Iter 1: sum=101^011=110 (6), carry=(101&011)<<1=010 (2)
Iter 2: sum=110^010=100 (4), carry=(110&010)<<1=100 (4)
Iter 3: sum=100^100=000 (0), carry=(100&100)<<1=1000 (8)
Iter 4: sum=000^1000=1000 (8), carry=0 → return 8
```

Wait — 5+3=8. Good.

---

### Template 5 — Power of 2

```text
return n > 0 AND (n AND (n - 1)) == 0
```

`n-1` flips trailing zeros and the lowest 1. `n & (n-1)` clears the lowest set bit. Powers of 2 have exactly one set bit.

---

## 5. Operations & Bit Invariants

### Operator reference

| Op | Meaning | Example |
|----|---------|---------|
| `&` | AND — 1 only if both bits 1 | `5 & 3` → `1` |
| `\|` | OR — 1 if either bit 1 | `5 \| 3` → `7` |
| `^` | XOR — 1 if bits differ | `5 ^ 3` → `6` |
| `~` | NOT — flip all bits | `~5` → `-6` |
| `<<` | Left shift — multiply by 2^k | `5 << 1` → `10` |
| `>>` | Arithmetic right shift — sign extends | `-1 >> 1` → `-1` |
| `>>>` | Logical right shift — zero-fill | `-1 >>> 1` → `2147483647` |

### XOR laws (memorize for interviews)

```text
a ^ a = 0
a ^ 0 = a
a ^ b = b ^ a          (commutative)
(a ^ b) ^ c = a ^ (b ^ c)  (associative)
```

### `n & (n - 1)` invariant

Always **removes the lowest set bit**:

```text
n     = 12  →  1100
n-1   = 11  →  1011
n&(n-1)     →  1000  (12 → 8)
```

Use for: count bits, power-of-2 test, iterate set bits.

---

## 6. Java Implementation Notes

### `>>` vs `>>>`

```java
int n = -1;
n >> 1;   // -1  (sign bit preserved)
n >>> 1;  // 2147483647 (zero-fill)
```

For **LC #191**, prefer `n >>>= 1` when shifting right to avoid infinite loop on negatives.

### No unsigned `int`

Java `int` is always signed. For bit problems, treat bits as unsigned when shifting:

```java
// Count bits — safe for negative n per LeetCode constraints
public int hammingWeight(int n) {
    int count = 0;
    while (n != 0) {
        count += n & 1;
        n >>>= 1;
    }
    return count;
}
```

Or use Kernighan (works for negatives too in two's complement).

### `Integer.bitCount(n)`

Exists in Java — know it for discussion, **don't use in interviews** unless interviewer allows.

### LC #371 and 32-bit overflow

LeetCode says 32-bit integers; loop until `carry == 0`. Mask to 32 bits if needed:

```java
carry = (a & b) << 1;  // may overflow int — LeetCode accepts this pattern
```

Some solutions mask: `carry = (a & b) << 1 & 0xFFFFFFFF` — only if required.

### `&` vs `&&`

```java
if (n & 1) { }    // WRONG — int not boolean
if ((n & 1) == 1) { }  // correct
```

---

## 7. Complexity Summary

| Problem | Approach | Time | Space |
|---------|----------|------|-------|
| LC #136 | XOR | O(n) | O(1) |
| LC #191 | Kernighan | O(k) k = set bits | O(1) |
| LC #191 | Shift each bit | O(32) = O(1) | O(1) |
| LC #338 | Bit DP | O(n) | O(n) |
| LC #371 | Bitwise add loop | O(32) iterations max | O(1) |
| Brute HashSet (#136) | O(n) | O(n) | — |

---

## 8. Recognition Signals

Reach for bit manipulation when you see:

```text
✓ "Every element appears twice except one"
✓ "O(1) extra space" + uniqueness / pairing
✓ "Count number of 1 bits" / hamming weight
✓ "For every number from 0 to n, count bits"
✓ "Add two numbers without using + or -"
✓ "Is n a power of two?"
✓ "Toggle / set / clear bit at position k"
```

**Not bit manipulation:** problems solvable cleanly with HashMap — bits are optional optimization.

---

## 9. Common Mistakes

| Mistake | Fix |
|---------|-----|
| `>>` on negative `n` in shift loop | Use `>>>` or Kernighan |
| `n & 1` in `if` without `== 1` | Compare to 1 explicitly |
| Forgetting XOR identity | Pairs cancel — order doesn't matter |
| `#338` brute force per number | Use `dp[i>>1] + (i&1)` |
| `#371` one XOR only | Need loop until carry is 0 |
| Power of 2 without `n > 0` | `0 & (-1) == 0` falsely passes |
| Confusing bitwise and logical ops | `&` vs `&&`, `\|` vs `\|\|` |

---

## 10. Your Progress & Problem Order

```text
Phase 1 complete:  Arrays ✅  Two Pointers ✅  Sliding Window ✅
Binary Search:     9/10  (LC #4 capstone left — do Sat/weekend)
Bit Manipulation:  0/4   ← YOU ARE HERE
```

### Solve in this order

| Order | Row | Problem | LC# | Variant | Why this order |
|-------|-----|---------|-----|---------|----------------|
| 1 | 31 | Single Number | 136 | XOR | Core trick — 5 min once you know XOR |
| 2 | 32 | Number of 1 Bits | 191 | Kernighan | Most common bit interview question |
| 3 | 33 | Counting Bits | 338 | Bit DP | Builds on #191 insight |
| 4 | 34 | Sum of Two Integers | 371 | Bitwise add | Deepest — save for last |

### LC #4 (Median) — don't skip

Finish Binary Search **before** or **in parallel**:

```text
Sat:  LC #4 capstone (closes BS 10/10)
      + Bit Manipulation #136, #191 if energy
```

Bit Manipulation is only **4 problems** — one focused session closes the pattern.

---

## Quick reference card

```text
XOR unique:     ans ^= x
Count bits:     while (n) { n &= n-1; count++; }
Bit DP:         dp[i] = dp[i>>1] + (i&1)
Add w/o +:      while (b) { carry=(a&b)<<1; a^=b; b=carry; }
Power of 2:     n>0 && (n&(n-1))==0
Set bit k:      n | (1 << k)
Clear bit k:    n & ~(1 << k)
Test bit k:     (n & (1 << k)) != 0
```

---

**Next step:** Read this guide, then solve **LC #136 Single Number** (no LeetCode until you've read sections 1–6). Say `LC #136` when ready to implement — guide mode, you code, I review.
