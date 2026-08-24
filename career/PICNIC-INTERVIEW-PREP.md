# Picnic Interview Prep — Hands-On Coding

> **Role:** Software Engineer - Store | Amsterdam, Netherlands  
> **Status:** Screening passed (2026-08-24) — 4 rounds pending  
> **Recruiter:** Thomas Carrillo Beeck  
> **Focus:** Write code by hand, debug under pressure, pair programming speed

---

## Interview Process

| Round | Format | What they test |
|-------|--------|----------------|
| **R1** | 1 developer | Technical deep-dive — projects, Java, distributed systems |
| **R2** | 2 developers | Live coding — read codebase, find bug, fix it |
| **R3** | Peer programming | Build/extend feature together — collaboration + coding |
| **R4** | Closing | Motivation, culture, visa/relocation, comp |

**This is NOT LeetCode-heavy.** Rounds 2 and 3 need **Java muscle memory without IDE autocomplete.**

---

## Daily Practice Block (Non-Negotiable Until Rounds Complete)

**45 minutes/day** — separate from DSA LeetCode time.

| Block | Time | Activity |
|-------|------|----------|
| Warm-up | 10 min | Write 1 small method by hand (no IDE) — collections, streams, or simple logic |
| Main | 25 min | 1 bug-fix OR 1 pair-programming extension exercise |
| Cool-down | 10 min | Explain solution out loud + note mistakes in log below |

### Rules
1. **No autocomplete** — paper, plain text editor, or IDE with suggestions off
2. **Talk while coding** — narrate every decision
3. **Speed target:** complete a 15-line fix in **under 20 minutes** by end of Week 2
4. **Done criteria:** code compiles in your head + you can explain edge cases

---

## Weekly Targets

### Week 1 (Aug 25–31) — Rebuild Hand-Coding Muscle
- [ ] 7 hand-written methods (1/day)
- [ ] 4 bug-fix exercises completed
- [ ] Red Hat + Vodafone architecture notes (1 page each, for R1)
- [ ] 1 mock R1 deep-dive out loud (30 min)

### Week 2 (Sep 1–7) — Bug Fix + Spring Patterns
- [ ] 4 bug-fix exercises (Java service layer)
- [ ] 2 pair-programming mocks (extend REST endpoint + add validation)
- [ ] Spring Boot: Controller → Service → Repository pattern written from memory once
- [ ] 1 timed bug-fix under 20 min

### Before Each Round
- [ ] R1: Project stories ready (STAR + technical depth)
- [ ] R2: 3 bug-fix drills in last 48 hours
- [ ] R3: 1 pair-programming mock in last 48 hours
- [ ] R4: Why Picnic, visa timeline, 3 questions for them

---

## Exercise Log

| # | Date | Type | Topic | Time | Pass? | Notes |
|---|------|------|-------|------|-------|-------|
| 1 | 2026-08-24 | Bug fix | OrderService (3 bugs) | — | ✅ Pass | Loops, Optional, boundary — all correct |
| 2 | | | | | | |
| 3 | | | | | | |

---

## Exercise 1 — Bug Fix (Round 2 Style)

Find and fix **3 bugs**. Write corrected methods by hand.

```java
public class OrderService {

    private final OrderRepository orderRepository;

    public OrderService(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }

    public double calculateTotal(List<OrderItem> items) {
        double total = 0;
        for (int i = 0; i <= items.size(); i++) {
            OrderItem item = items.get(i);
            total += item.getPrice() * item.getQuantity();
        }
        return total;
    }

    public Optional<Order> findLatestOrder(String customerId) {
        List<Order> orders = orderRepository.findByCustomerId(customerId);
        if (orders.isEmpty()) {
            return null;
        }
        return Optional.of(orders.get(orders.size()));
    }

    public boolean isEligibleForFreeDelivery(double orderTotal) {
        return orderTotal > 50.0;
    }
}
```

<details>
<summary>Hints (don't open until you try)</summary>

1. Loop bounds — off-by-one / `IndexOutOfBoundsException`
2. `Optional` — never return `null`; wrong index for "latest"
3. Free delivery — boundary: is exactly €50 eligible?

</details>

---

## Exercise Types to Rotate

| Type | Example | Picnic round |
|------|---------|--------------|
| Bug fix | NPE, wrong loop, bad Optional usage | R2 |
| Logic fix | Wrong comparison, missing edge case | R2 |
| Extend API | Add field validation to DTO + service | R3 |
| Small feature | `applyDiscount`, `filterInStockItems` | R3 |
| Read + explain | Trace request through 3 classes | R1, R2 |

---

## R1 Prep — Technical Deep-Dive Topics

Be ready to go 3 levels deep:

| Topic | Your story |
|-------|------------|
| Event-driven systems | Harbor — Kafka pipelines, latency reduction |
| Scale | Vodafone — 30M customer migration |
| Trade-offs | Why Kafka vs sync REST, idempotency, failure handling |
| Java | Collections choice, concurrency basics, Spring Boot structure |

---

## Mentor Commands

- **`Picnic prep`** — today's hands-on exercise + R1 talking points
- **`Bug fix`** — new Round 2 style exercise
- **`Pair mock`** — simulate Round 3 live coding session
- **`Done`** — log exercise in table above + critique

---

## Links

- [Picnic Study Guide](./interview-prep/PICNIC-STUDY-GUIDE.md) — JD, interview process, round-by-round prep
- [Java & Spring Revision](./interview-prep/JAVA-SPRING-REVISION.md) — generic backend interview revision
- [Application Tracker](./APPLICATION-TRACKER.md) — Picnic row #16
- [Backend Roadmap](../BACKEND-ENGINEER-ROADMAP.md) — Track 6: Hands-On Interview Coding
- [Picnic Tech Jobs](https://jobs.picnic.app/en/tech)
