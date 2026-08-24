# Java & Spring — Interview Revision Guide

> **Purpose:** Quick revision before backend interviews (Picnic, product companies, FAANG-adjacent).  
> **How to use:** Read one section per day. For each topic, you should be able to **explain + give a real example from Red Hat/Vodafone**.

---

## Table of Contents

1. [Java Core](#1-java-core)
2. [Collections & Streams](#2-collections--streams)
3. [Concurrency Basics](#3-concurrency-basics)
4. [JVM & Memory (Interview Level)](#4-jvm--memory-interview-level)
5. [Spring Boot Fundamentals](#5-spring-boot-fundamentals)
6. [Spring Advanced (Senior Rounds)](#6-spring-advanced-senior-rounds)
7. [REST APIs & HTTP](#7-rest-apis--http)
8. [Databases & JPA](#8-databases--jpa)
9. [Kafka & Messaging](#9-kafka--messaging)
10. [Testing & Code Quality](#10-testing--code-quality)
11. [Common Bug Patterns (Live Coding)](#11-common-bug-patterns-live-coding)
12. [Quick Interview Q&A](#12-quick-interview-qa)

---

## 1. Java Core

### OOP Pillars
| Pillar | One-liner | Example |
|--------|-----------|---------|
| Encapsulation | Hide state, expose behavior | Private fields + getters/setters |
| Inheritance | IS-A relationship | `class Dog extends Animal` |
| Polymorphism | Same interface, different behavior | `List` = `ArrayList` or `LinkedList` |
| Abstraction | Hide complexity | `interface PaymentGateway` |

### equals() and hashCode()
- **Contract:** If `a.equals(b)` → same `hashCode()`. Reverse not required.
- **Why:** `HashMap`/`HashSet` use hash bucket first, then `equals()` for collision.
- **Bug pattern:** Override `equals` but not `hashCode` → broken `HashSet` behavior.

```java
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof OrderItem other)) return false;
    return Objects.equals(this.sku, other.sku);
}

@Override
public int hashCode() {
    return Objects.hash(sku);
}
```

### String
- **Immutable** — every modification creates new object.
- **String pool** — literals interned; `new String("x")` is separate.
- Use `StringBuilder` for loops; never `str +=` in a loop.

### Optional
- Never return `null` from `Optional` method → use `Optional.empty()`.
- Don't use `Optional` as field type (usually).
- Prefer `orElseThrow()`, `map()`, `flatMap()` over `get()`.

### Exception Handling
- **Checked** — compiler forces handle (`IOException`).
- **Unchecked** — `RuntimeException` (`NullPointerException`, `IllegalArgumentException`).
- Catch specific exceptions; don't swallow empty `catch`.

---

## 2. Collections & Streams

### When to use what
| Structure | Use when | Time complexity |
|-----------|----------|-----------------|
| `ArrayList` | Random access, iteration | get: O(1), insert middle: O(n) |
| `LinkedList` | Frequent insert/delete at ends | get: O(n) |
| `HashMap` | Key-value lookup | avg O(1) |
| `TreeMap` | Sorted keys | O(log n) |
| `HashSet` | Unique elements | avg O(1) |
| `PriorityQueue` | Top K, scheduling | insert: O(log n) |

### HashMap internals (must know)
- Array of buckets → each bucket = linked list or tree (Java 8+).
- `hash(key) % capacity` → bucket index.
- Load factor 0.75 → resize when 75% full.
- **Not thread-safe** → use `ConcurrentHashMap` in multi-threaded code.

### Streams
```java
// Filter + map + collect — know this cold
List<String> names = orders.stream()
    .filter(o -> o.getTotal() > 50)
    .map(Order::getCustomerName)
    .distinct()
    .sorted()
    .collect(Collectors.toList());
```
- **Lazy** until terminal operation.
- Don't mutate external state inside stream (side effects).
- `parallelStream()` — only for CPU-heavy, large data; understand overhead.

---

## 3. Concurrency Basics

### Key concepts
| Concept | Meaning |
|---------|---------|
| `synchronized` | Mutual exclusion on object/method |
| `volatile` | Visibility guarantee (not atomicity) |
| `ThreadLocal` | Per-thread variable copy |
| `ExecutorService` | Thread pool abstraction |

### Common interview questions
- **Why is HashMap not thread-safe?** Two threads put → infinite loop / lost update (pre-Java 8).
- **ConcurrentHashMap vs synchronized Map?** Finer-grained locking / CAS segments.
- **Deadlock?** Thread A holds lock1, wants lock2; Thread B holds lock2, wants lock1.

### Producer-Consumer pattern
- `BlockingQueue` — producer puts, consumer takes; blocks when full/empty.
- Maps to Kafka consumer groups conceptually.

---

## 4. JVM & Memory (Interview Level)

### Heap structure (simplified)
```
Heap: Young Gen (Eden + Survivor) → Old Gen
      Metaspace (class metadata)
Stack: per-thread frames (local variables, method calls)
```

### Garbage Collection
- **Minor GC** — Young gen, frequent, fast.
- **Major/Full GC** — Old gen, pauses application (STW).
- **G1GC** — default in modern Java; targets predictable pauses.

### Interview one-liner
> "I monitor GC pauses and heap usage in production via metrics. For our services, we tune heap size and watch for memory leaks in long-lived caches."

---

## 5. Spring Boot Fundamentals

### Architecture layers
```
Controller  →  Service  →  Repository  →  Database
   (HTTP)      (business)    (data access)
```

### Dependency Injection
- **Constructor injection** (preferred) — immutable, testable.
- `@Autowired` on constructor — Spring injects beans.
- `@Component`, `@Service`, `@Repository` — stereotypes.

```java
@Service
public class OrderService {
    private final OrderRepository repo;

    public OrderService(OrderRepository repo) {  // constructor injection
        this.repo = repo;
    }
}
```

### Bean scopes
| Scope | When |
|-------|------|
| `singleton` | Default — one instance per container |
| `prototype` | New instance every injection |
| `request` / `session` | Web scopes |

### Application properties
- `application.yml` / `application.properties`
- Profiles: `application-dev.yml`, `application-prod.yml`
- `@Value("${app.name}")` or `@ConfigurationProperties`

### REST Controller pattern
```java
@RestController
@RequestMapping("/api/orders")
public class OrderController {

    private final OrderService orderService;

    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    @GetMapping("/{id}")
    public ResponseEntity<OrderDto> getOrder(@PathVariable Long id) {
        return orderService.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<OrderDto> create(@Valid @RequestBody CreateOrderRequest req) {
        OrderDto created = orderService.create(req);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }
}
```

---

## 6. Spring Advanced (Senior Rounds)

### @Transactional
- Proxy-based AOP — external call works; **self-call within same class does NOT**.
- `propagation`: REQUIRED (default), REQUIRES_NEW, NESTED.
- `readOnly = true` — optimization hint for queries.
- Rollback on **unchecked** exceptions by default.

### Bean lifecycle (short)
1. Instantiate → 2. Inject dependencies → 3. `@PostConstruct` → 4. Ready → 5. `@PreDestroy` on shutdown.

### Spring Boot auto-configuration
- `@SpringBootApplication` = `@Configuration` + `@EnableAutoConfiguration` + `@ComponentScan`.
- Conditions on classpath trigger auto-config (e.g., `DataSource` if JDBC driver present).

---

## 7. REST APIs & HTTP

### HTTP methods
| Method | Idempotent? | Safe? | Use |
|--------|-------------|-------|-----|
| GET | Yes | Yes | Read |
| POST | No | No | Create |
| PUT | Yes | No | Full replace |
| PATCH | No | No | Partial update |
| DELETE | Yes | No | Remove |

### Status codes (know these)
- `200` OK, `201` Created, `204` No Content
- `400` Bad Request, `401` Unauthorized, `403` Forbidden, `404` Not Found
- `409` Conflict, `422` Validation error
- `500` Internal Server Error, `503` Service Unavailable

### API design principles
- Nouns for resources: `/orders`, `/orders/{id}/items`
- Versioning: `/api/v1/orders` or header-based
- Pagination: `?page=0&size=20` or cursor-based
- Idempotency keys for POST (payments, orders)

---

## 8. Databases & JPA

### SQL essentials
- **JOINs:** INNER (match both), LEFT (all left + matching right), FULL.
- **Indexes:** Speed reads, slow writes; use on WHERE/JOIN columns.
- **Transactions:** ACID — Atomicity, Consistency, Isolation, Durability.

### Isolation levels
| Level | Dirty read | Non-repeatable read | Phantom read |
|-------|------------|---------------------|--------------|
| READ UNCOMMITTED | Yes | Yes | Yes |
| READ COMMITTED | No | Yes | Yes |
| REPEATABLE READ | No | No | Yes |
| SERIALIZABLE | No | No | No |

### JPA / Hibernate — N+1 problem
```java
// BAD: 1 query for orders + N queries for items
List<Order> orders = orderRepo.findAll();
orders.forEach(o -> o.getItems().size());  // lazy load each

// FIX: JOIN FETCH or @EntityGraph
@Query("SELECT o FROM Order o JOIN FETCH o.items WHERE o.id = :id")
Optional<Order> findWithItems(@Param("id") Long id);
```

### MongoDB vs PostgreSQL (Picnic uses both)
| | PostgreSQL | MongoDB |
|---|------------|---------|
| Model | Relational, schema | Document, flexible schema |
| Joins | Native SQL joins | `$lookup` or denormalize |
| Transactions | Full ACID | Multi-doc transactions (4.0+) |
| Use case | Structured data, reporting | Flexible catalogs, rapid iteration |

---

## 9. Kafka & Messaging

### Core concepts
| Term | Meaning |
|------|---------|
| Topic | Category of events |
| Partition | Ordered log within topic; parallelism unit |
| Offset | Position in partition |
| Consumer group | Consumers share load; one consumer per partition |
| Broker | Kafka server |

### Why Kafka over REST for async?
- **Decoupling** — producer doesn't wait for consumer.
- **Buffering** — handle traffic spikes.
- **Replay** — consumers re-read from offset.
- **Multiple consumers** — same event, different services.

### Delivery semantics
| Guarantee | Meaning |
|-----------|---------|
| At-most-once | May lose messages |
| At-least-once | May duplicate (need idempotency) |
| Exactly-once | Hardest; transactional producer + idempotent consumer |

### Your Harbor story (template)
> "We use Kafka for event-driven sync between Harbor and downstream systems. Producers publish domain events; consumers process with at-least-once semantics. We handle duplicates with idempotent keys and offset management."

---

## 10. Testing & Code Quality

### Test pyramid
```
        /  E2E  \        few, slow
       / Integration \    some
      /   Unit tests   \  many, fast
```

### JUnit basics
```java
@Test
void calculateTotal_emptyList_returnsZero() {
    OrderService service = new OrderService(mockRepo);
    assertEquals(0.0, service.calculateTotal(List.of()));
}

@Test
void findLatestOrder_noOrders_returnsEmpty() {
    when(mockRepo.findByCustomerId("c1")).thenReturn(List.of());
    assertTrue(service.findLatestOrder("c1").isEmpty());
}
```

### Mockito
- `when(repo.findById(1L)).thenReturn(Optional.of(order));`
- `verify(repo, times(1)).save(any());`

---

## 11. Common Bug Patterns (Live Coding)

Practice finding these without IDE:

| Bug type | Example | Fix |
|----------|---------|-----|
| Off-by-one | `i <= list.size()` | `i < list.size()` |
| Null return | `return null` from `Optional` method | `Optional.empty()` |
| Wrong index | `list.get(list.size())` | `list.get(list.size() - 1)` |
| Boundary | `total > 50` for "≥ 50" | `total >= 50` |
| NPE in map | `map.get(key) + 1` when key missing | `map.merge(key, 1, Integer::sum)` or `getOrDefault` |
| Empty list | `list.get(0)` without check | Guard `isEmpty()` first |
| equals without hashCode | Custom object in HashSet | Override both |

---

## 12. Quick Interview Q&A

### Java
**Q: ArrayList vs LinkedList?**  
A: ArrayList — O(1) random access, better cache locality. LinkedList — O(1) insert at ends, worse random access. Default to ArrayList.

**Q: Why is String immutable?**  
A: Security (passwords in pool), thread safety, hash caching, string interning.

**Q: Checked vs unchecked exceptions?**  
A: Checked must be declared/handled; unchecked are programming errors. Prefer specific runtime exceptions for APIs.

### Spring
**Q: How does Spring DI work?**  
A: IoC container scans components, creates beans, resolves dependencies via constructor/setter injection, manages lifecycle.

**Q: @Component vs @Service vs @Repository?**  
A: Same mechanism; semantic difference. Repository adds exception translation for persistence.

### System design (short)
**Q: How do you ensure idempotency?**  
A: Idempotency key per request, store processed keys in DB/Redis, return same response on retry.

**Q: Cache-aside pattern?**  
A: Read: check cache → miss → read DB → write cache. Write: update DB → invalidate cache.

---

## Revision Schedule (7 days)

| Day | Topics |
|-----|--------|
| 1 | Java Core + Collections |
| 2 | Streams + Optional + bug patterns |
| 3 | Spring Boot layers + REST |
| 4 | @Transactional + JPA/N+1 |
| 5 | Kafka + messaging |
| 6 | Concurrency + JVM basics |
| 7 | Full mock Q&A — explain everything out loud |

---

## Your Projects — Map Topics

| Topic | Red Hat (Harbor) | Vodafone (Solstice) |
|-------|------------------|---------------------|
| Event-driven | Kafka pipelines | Lifecycle event workflows |
| Scale | High-throughput data sync | 30M customer migration |
| Java/Spring | Microservices, REST APIs | Multithreaded services |
| Reliability | Production on OpenShift/K8s | 40+ configurable workflows |
| Trade-offs | Kafka vs sync, latency vs consistency | Batch vs real-time processing |

---

*Linked from: [PICNIC-STUDY-GUIDE.md](./PICNIC-STUDY-GUIDE.md) | [PICNIC-INTERVIEW-PREP.md](../PICNIC-INTERVIEW-PREP.md)*
