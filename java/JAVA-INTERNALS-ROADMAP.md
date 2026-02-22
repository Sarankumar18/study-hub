# Java Internals Mastery Roadmap

> **Goal:** Not "I can clear 1Z0-829" — but "I know why this production thread pool just deadlocked."

**Timeline:** 8–12 weeks depending on pace (2–3 hrs/day = ~9 weeks, 1–2 hrs/day = ~12 weeks)

**Strategy:** Spend 8–10 weeks learning deeply, then 1 week revision for 1Z0-829. Knowledge first, certification second.

---

## Phase 1 — Language Mastery (Weeks 1–4)

**Why this matters:** Most Java devs know syntax. You need to understand what the JVM actually does with your code.

### Topics

| Topic | What to Understand | How to Verify |
|-------|-------------------|---------------|
| Generics | Type erasure, PECS, wildcards, covariance/contravariance | `javap -c` your generic class — see the casts |
| Streams | Lazy evaluation, pipeline fusion, intermediate vs terminal | Write a stream with `.peek()` — observe evaluation order |
| Functional Interfaces | Lambda desugaring, method reference bytecode | `javap -c` — see `invokedynamic` + `LambdaMetafactory` |
| Records | JVM storage, auto-generated methods | `javap -c` a Record — see the constructor, accessors, equals/hashCode |
| Sealed Classes | Class loading restrictions, `permits` enforcement | Try extending a sealed class from another package |
| Comparator | Contract violations (transitivity, consistency with equals) | Write a broken comparator — watch `TimSort` throw `IllegalArgumentException` |
| Optional | Why not for fields, why not serializable | Read Bloch's reasoning — it's a return-type-only construct |
| Switch Expressions | Compiled form, pattern matching desugaring | `javap -c` a switch expression — see the `tableswitch`/`lookupswitch` |

### Hands-On Exercise

```bash
# Compile and inspect bytecode for any class
javac MyClass.java
javap -c MyClass.class

# See how a lambda becomes invokedynamic
javap -c -p MyLambdaClass.class
```

### Resources

#### Books

1. **Effective Java** — Joshua Bloch (3rd Edition)
   - *The* book on how senior Java engineers think
   - Covers: immutability, equals/hashCode contract, builder pattern, enum usage, defensive copying, generics best practices, composition over inheritance
   - [Amazon](https://www.amazon.com/Effective-Java-Joshua-Bloch/dp/0134685997)

2. **Java Generics and Collections** — Maurice Naftalin & Philip Wadler
   - The only proper deep book on generics
   - Covers: `List<Object>` vs `List<String>`, PECS rule, wildcards, type erasure, covariance/contravariance
   - [O'Reilly](https://www.oreilly.com/library/view/java-generics-and/0596527756/)

#### Videos

3. **"Java Streams in Depth"** — Venkat Subramaniam
   - Search: *"Venkat Subramaniam Java Streams"* on YouTube
   - Covers: lazy evaluation, pipeline fusion, performance traps
   - After this you'll stop using `.parallelStream()` randomly

#### Supplementary

- **Java Language Specification (JLS)** — [docs.oracle.com/javase/specs](https://docs.oracle.com/javase/specs/)
  - Not a reading book — use as a reference when you want to know *exactly* what the spec says
- **Baeldung** — [baeldung.com](https://www.baeldung.com/)
  - Great for quick, focused deep-dives on specific topics (generics, streams, records, etc.)

---

## Phase 2 — Concurrency (Weeks 5–9)

**Why this matters:** You're building pricing engines, Kafka consumers, API services. This is where 90% of Java devs fail. This is where production bugs live.

### Core Concepts (Week 5–6)

| Topic | What to Understand |
|-------|-------------------|
| Thread lifecycle | NEW → RUNNABLE → BLOCKED → WAITING → TIMED_WAITING → TERMINATED |
| `synchronized` vs `Lock` | Intrinsic monitor vs ReentrantLock, fairness, tryLock, interruptibility |
| `volatile` | Visibility guarantee, no atomicity, when it's enough vs when it's not |
| Happens-before | The formal ordering rule that governs all multithreaded correctness |
| Visibility vs atomicity | Why `volatile int count` still loses increments under contention |

### Advanced (Week 7–9)

| Topic | What to Understand |
|-------|-------------------|
| ExecutorService | Thread pool lifecycle, shutdown vs shutdownNow |
| Callable vs Runnable | Return values, exception propagation |
| ThreadPool tuning | Core size, max size, queue type, rejection policy |
| ForkJoinPool | Work stealing, common pool shared by parallel streams |
| CompletableFuture | Async composition, thenApply vs thenCompose, exception handling |
| Parallel streams | Uses ForkJoinPool.commonPool() — why this kills Tomcat threads |

### Understand These Data Structures

| Structure | Why It Matters |
|-----------|---------------|
| `ConcurrentHashMap` | Segmented locking (Java 7) → bucket-level CAS (Java 8+) — no global lock |
| `CopyOnWriteArrayList` | Fast reads, slow writes — good for event listeners, bad for frequent mutations |
| `BlockingQueue` | Producer-consumer backbone — used in thread pools internally |

### Resources

#### Books

4. **Java Concurrency in Practice** — Brian Goetz
   - **Your backend engineer bible**
   - Covers: happens-before, visibility vs atomicity, race conditions, thread safety, safe publication, locking strategies, executor framework, ConcurrentHashMap internals
   - [Amazon](https://www.amazon.com/Java-Concurrency-Practice-Brian-Goetz/dp/0321349601)
   - Every Kafka consumer / Pricing engine needs this knowledge

#### Videos

5. **"Java Memory Model Explained"** — Aleksey Shipilev
   - Search: *"Aleksey Shipilev JMM"* on YouTube
   - Covers: volatile, instruction reordering, CPU cache effects, memory visibility
   - Explains the bug: "Why is the value updated in one thread not visible in another?"

#### Supplementary

- **JSR-133 FAQ** — [cs.umd.edu/~pugh/java/memoryModel/jsr-133-faq.html](https://www.cs.umd.edu/~pugh/java/memoryModel/jsr-133-faq.html)
  - The original Java Memory Model explanation by the people who designed it
- **Doug Lea's concurrency page** — [gee.cs.oswego.edu/dl/concurrency-interest](http://gee.cs.oswego.edu/dl/concurrency-interest/)
  - Doug Lea wrote `java.util.concurrent` — this is the source

---

## Phase 3 — JVM Internals (Weeks 10–12)

**Why this matters:** This is FAANG-level backend knowledge. This is what separates "I write Java" from "I understand the machine running my Java."

### Topics

| Topic | What to Understand |
|-------|-------------------|
| Heap vs Stack | Stack = per-thread, method frames; Heap = shared, GC-managed objects |
| Eden / Survivor / Old Gen | Young gen allocation, promotion thresholds, tenuring |
| G1 GC | Region-based, pause-time target, mixed collections |
| ZGC | Sub-millisecond pauses, colored pointers, concurrent relocation |
| Parallel GC | Throughput-optimized, stop-the-world young + old |
| Stop-The-World | Why all GCs pause, what triggers it, how to minimize it |
| Escape analysis | JVM proves object doesn't escape method → stack-allocates it |
| JIT compilation | C1 (client) vs C2 (server), tiered compilation, OSR |
| Class loading | Bootstrap → Extension → Application, delegation model |

### Hands-On: Run These on Your Spring Boot App

```bash
# GC logging (Java 11+)
java -Xlog:gc*:file=gc.log:time,uptime,level,tags -jar your-app.jar

# GC logging (Java 8)
java -XX:+PrintGCDetails -XX:+PrintGCDateStamps -jar your-app.jar

# Monitor live
jvisualvm     # Visual profiler — heap, threads, CPU
jconsole      # JMX-based monitoring
jcmd <pid> GC.heap_info          # Heap breakdown
jcmd <pid> Thread.print          # Thread dump
jcmd <pid> VM.flags              # Active JVM flags

# Flight Recorder (production-safe profiling)
jcmd <pid> JFR.start duration=60s filename=recording.jfr
```

### What to Observe

- **Memory usage** — Is old gen growing? Are you creating too many short-lived objects?
- **Thread count** — Are threads leaking? Is the pool sized correctly?
- **GC pause time** — Are STW pauses affecting latency?
- **Allocation rate** — High allocation rate = more GC pressure

### Resources

#### Books

6. **Understanding the JVM: Advanced Features and Best Practices** — Zhou Zhiming
   - Covers: heap layout, stack frames, GC lifecycle, class loading, JIT compilation, escape analysis
   - [Amazon](https://www.amazon.com/Understanding-Java-Virtual-Machine-Advanced/dp/9811503834)

#### Videos

7. **"JVM Anatomy Quarks"** — Aleksey Shipilev
   - Search: *"JVM Anatomy Quarks"* or visit [shipilev.net/jvm/anatomy-quarks](https://shipilev.net/jvm/anatomy-quarks/)
   - Mind-blowing deep dives on: object allocation, GC pauses, lock contention, CPU cache-line false sharing
   - These are short, focused essays — perfect for daily reading

#### Supplementary

- **GC Handbook** — [plumbr.io/java-garbage-collection-handbook](https://plumbr.io/java-garbage-collection-handbook) (free)
- **JVM Internals Blog** — [blog.jamesdbloom.com/JVMInternals.html](https://blog.jamesdbloom.com/JVMInternals.html)
  - Single-page visual walkthrough of class file format, stack frames, memory layout

---

## Phase 4 — I/O + NIO (Weeks 12–13)

**Why this matters:** This explains why Netty is faster than traditional servlet I/O, and why reactive frameworks exist.

### Topics

| Topic | What to Understand |
|-------|-------------------|
| Blocking I/O | Thread-per-connection model, why it doesn't scale |
| Non-blocking I/O | Selector + Channel + Buffer pattern |
| Selector | Multiplexing — one thread monitors many channels |
| Channel | Bidirectional, connects to file/socket/pipe |
| Buffer | Direct vs heap buffers, flip/compact/clear lifecycle |
| Memory-mapped files | `MappedByteBuffer` — OS-level page cache, zero-copy |

### Key Insight

```
Traditional Servlet:  1 request = 1 thread (blocked on I/O)
NIO / Netty:          1 thread = many connections (event loop)
```

This is why Netty, gRPC, and reactive stacks exist.

### Resources

#### Books

8. **Java NIO** — Ron Hitchens
   - Covers: Channels, Buffers, Selectors, blocking vs non-blocking I/O
   - [O'Reilly](https://www.oreilly.com/library/view/java-nio/0596002882/)

#### Supplementary

- **Netty in Action** — Norman Maurer (if you want to understand how NIO is used in production frameworks)
- Baeldung NIO series — clear, code-heavy tutorials

---

## Phase 5 — JDBC + Transactions (Weeks 14–15)

**Why this matters:** Directly relevant to your Harbor pricing platform — SKU pricing writes, overrides logic, connection management under load.

### Topics

| Topic | What to Understand |
|-------|-------------------|
| Auto-commit | Default is `true` — every statement is its own transaction |
| Isolation levels | READ_UNCOMMITTED → READ_COMMITTED → REPEATABLE_READ → SERIALIZABLE |
| Phantom reads | Why REPEATABLE_READ doesn't prevent range-query anomalies |
| Connection pooling | Why creating connections is expensive, how pools recycle them |
| HikariCP | Why it's the fastest — ConcurrentBag, lock-free design, connection validation |
| Batch operations | `addBatch()` + `executeBatch()` — 10-100x faster for bulk writes |

### Resources

#### Books

9. **High-Performance Java Persistence** — Vlad Mihalcea
    - **The** book for DB performance in Java
    - Covers: isolation levels, transaction boundaries, connection pooling, batch inserts, DB locks, phantom reads
    - [vladmihalcea.com](https://vladmihalcea.com/books/high-performance-java-persistence/)
    - Vlad also has an excellent blog with free articles on every topic

---

## Post-Roadmap (Optional, Elite-Level)

### Book

10. **Java Performance: In-Depth Advice for Tuning and Programming** — Scott Oaks (2nd Edition)
    - Covers: GC tuning, JIT compiler internals, CPU profiling, allocation rate impact
    - Read this after Phase 3 when you have context to appreciate it
    - [O'Reilly](https://www.oreilly.com/library/view/java-performance-2nd/9781492056102/)

---

## Resource Summary

| # | Resource | Type | Phase | Priority |
|---|----------|------|-------|----------|
| 1 | Effective Java — Joshua Bloch | Book | 1 | Must Read |
| 2 | Java Generics and Collections — Naftalin | Book | 1 | Deep Dive |
| 3 | Venkat Subramaniam — Streams Talk | Video | 1 | Must Watch |
| 4 | Java Concurrency in Practice — Brian Goetz | Book | 2 | **Critical** |
| 5 | Aleksey Shipilev — JMM Talk | Video | 2 | Must Watch |
| 6 | Understanding the JVM — Zhou Zhiming | Book | 3 | Must Read |
| 7 | JVM Anatomy Quarks — Aleksey Shipilev | Essays | 3 | Must Read |
| 8 | Java NIO — Ron Hitchens | Book | 4 | Good to Know |
| 9 | High-Performance Java Persistence — Vlad Mihalcea | Book | 5 | **Critical** |
| 10 | Java Performance — Scott Oaks | Book | Post | Elite |

---

## Suggested Fast-Track Stack (Top 5 to Start)

If time is limited, start with these — they directly improve Spring Boot apps, Kafka consumers, pricing engines, thread pools, and DB writes:

1. **Effective Java** — foundation of thinking like a senior Java engineer
2. **Venkat Subramaniam Streams talk** — stops you from writing slow stream code
3. **Java Concurrency in Practice** — prevents every concurrency bug you'll ever hit
4. **JVM Anatomy Quarks** — makes GC and performance intuitive
5. **High-Performance Java Persistence** — makes your DB layer production-grade

---

## Weekly Schedule Template

| Week | Phase | Focus | Resource |
|------|-------|-------|----------|
| 1 | 1 | Generics, Type Erasure, PECS | Effective Java (Ch. 5), Generics book |
| 2 | 1 | Streams, Lambdas, Functional Interfaces | Venkat's talk, Effective Java (Ch. 7) |
| 3 | 1 | Records, Sealed Classes, Switch Expressions | JLS, `javap -c` exercises |
| 4 | 1 | Collections deep dive, Comparator contracts | Effective Java (Ch. 3, 4) |
| 5 | 2 | Thread lifecycle, synchronized, volatile | JCiP (Ch. 1–3) |
| 6 | 2 | Happens-before, visibility, JMM | JCiP (Ch. 16), Shipilev JMM talk |
| 7 | 2 | Executors, ThreadPool tuning | JCiP (Ch. 6–8) |
| 8 | 2 | CompletableFuture, ForkJoinPool | JCiP (Ch. 11), Java docs |
| 9 | 2 | Concurrent collections, parallel streams | JCiP (Ch. 5), Venkat's talk |
| 10 | 3 | Heap layout, GC types, GC logging | JVM book, Anatomy Quarks |
| 11 | 3 | JIT, escape analysis, class loading | JVM book, `jcmd` exercises |
| 12 | 3+4 | Profiling your app + NIO basics | jvisualvm, Java NIO book |
| 13 | 4+5 | NIO deep dive + JDBC/transactions | NIO book, Vlad Mihalcea |
| 14 | 5 | Connection pooling, HikariCP, batch ops | Vlad Mihalcea |
| 15 | — | **1Z0-829 Revision** | Enthuware mock tests + review |

---

## Free Online Resources

- **Shipilev's Blog** — [shipilev.net](https://shipilev.net/) — JVM performance god-tier content
- **Baeldung** — [baeldung.com](https://www.baeldung.com/) — practical Java tutorials
- **Vlad Mihalcea's Blog** — [vladmihalcea.com/blog](https://vladmihalcea.com/blog/) — free JPA/Hibernate/JDBC articles
- **James Bloom JVM Internals** — [blog.jamesdbloom.com/JVMInternals.html](https://blog.jamesdbloom.com/JVMInternals.html)
- **Plumbr GC Handbook** — [plumbr.io/java-garbage-collection-handbook](https://plumbr.io/java-garbage-collection-handbook)
- **Jenkov Concurrency Tutorials** — [jenkov.com/tutorials/java-concurrency](https://jenkov.com/tutorials/java-concurrency/index.html)
- **Enthuware** — [enthuware.com](https://enthuware.com/) — best mock tests for 1Z0-829 (cheap, high quality)

---

## How to Use `javap` (Your Secret Weapon)

```bash
# See what the JVM actually does with your code
javac MyClass.java
javap -c MyClass.class          # Bytecode
javap -c -p MyClass.class       # Include private members
javap -v MyClass.class          # Verbose — constant pool, flags, everything

# What to look for:
# - invokedynamic         → lambda/method reference desugaring
# - LambdaMetafactory     → how lambdas are wired at runtime
# - tableswitch/lookupswitch → switch compilation strategy
# - checkcast             → generics type erasure inserting casts
# - monitorenter/monitorexit → synchronized block implementation
```

---

*After completing this roadmap: certification becomes easy, system design interviews become easier, debugging production issues becomes logical.*
