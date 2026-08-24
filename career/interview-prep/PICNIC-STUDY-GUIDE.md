# Picnic — Complete Study Guide

> **Role:** Software Engineer - Store  
> **Location:** Amsterdam, Netherlands (office-first)  
> **Status:** Screening passed (2026-08-24) — 4 rounds pending  
> **Companion docs:** [JAVA-SPRING-REVISION.md](./JAVA-SPRING-REVISION.md) | [PICNIC-INTERVIEW-PREP.md](../PICNIC-INTERVIEW-PREP.md)

---

## 1. Company Overview

### What Picnic is
- **Online-only grocery supermarket** founded 2015 in the Netherlands.
- Delivers groceries with **own electric fleet** ("supermarket on wheels").
- Operates in **Netherlands, Germany, France** — millions of customers.
- **Engineering-first culture** — they build everything in-house: app, backend, warehouse systems, routing, ML.

> Candidates consistently say: *"Picnic is a tech company that happens to deliver groceries."*

### Why engineers join Picnic
- Full-stack ownership — product teams own features end-to-end
- Modern Java stack at scale
- International team (80+ nationalities)
- Visa sponsorship for skilled migrants (Netherlands)
- No Dutch language required

### Culture keywords (use in interviews)
- **Ownership** — end-to-end responsibility
- **Product mindset** — tech serves business problems
- **Collaboration** — cross-functional teams
- **Build from scratch** — not maintaining legacy cruft
- **Launch fast, iterate** — experimental mindset

**Sources:** [Picnic Careers](https://jobs.picnic.app/en/tech), [Relocate.me — Oscar's story](https://relocate.me/blog/expat-stories/moving-to-the-netherlands-for-an-it-job-oscars-relocation-story/)

---

## 2. Role: Software Engineer - Store

### Team: Consumer Domain
The **Store** team builds **customer-facing backend features** for the shopping experience:

| Feature area | What it means |
|--------------|---------------|
| Meal Planner | Personalized meal suggestions, recipe → grocery list |
| Loyalty programs | Rewards, retention, engagement |
| Personalization | Recommendations, shopping history |
| Order experience | Cart, checkout flows, product catalog backend |

**Your pitch:** Backend systems that millions of users interact with daily — not internal tooling.

### Job Description — Key Responsibilities
- Take **ownership** of projects from concept to production
- Build solutions that make shopping **smarter, faster, more intuitive**
- Work cross-functionally with Product, Frontend, Data Science
- Solve business problems with the **right technical solution** (product mindset)

### Requirements (from JD)
| Requirement | Your fit |
|-------------|----------|
| Master's or equivalent experience | MCA + 5 YoE ✅ |
| 2–5 years Java | 5 YoE ✅ |
| Product mindset | Harbor + Vodafone user-impact stories ✅ |
| Distributed systems familiarity | Kafka, microservices ✅ |
| English proficiency | ✅ |
| Relocate to Amsterdam | Committed ✅ |
| AI tooling comfort | Mention Cursor/AI-assisted dev if asked (optional plus) |

---

## 3. Tech Stack (Memorize This)

| Layer | Technologies |
|-------|-------------|
| **Backend** | Java 21, Spring 6, Spring Boot 3, Reactor, Immutables |
| **Frontend (collab)** | TypeScript, React, React Native |
| **Databases** | PostgreSQL, MongoDB |
| **Messaging** | Kafka, RabbitMQ |
| **Infra** | Docker, Kubernetes, AWS, Helm, Terraform, Vault |
| **Observability** | Datadog |
| **Build** | Maven, Git |
| **Other** | GraalVM, Apache Calcite, Python 3.x |

### What to emphasize in interviews
- **Java + Spring Boot** — your daily stack
- **Kafka** — event-driven at Red Hat
- **PostgreSQL** — relational data
- **Kubernetes/OpenShift** — production deployments
- **REST APIs** — microservices

### What to be honest about gaps
- **Reactor (reactive)** — read basics: `Mono`, `Flux`, non-blocking I/O concept
- **MongoDB** — document model vs SQL; when denormalization makes sense
- **TypeScript/React** — you collaborate with frontend, don't need to code it deeply

---

## 4. Interview Process

### Your confirmed pipeline (from Thomas, Aug 24)

| Round | Format | Focus |
|-------|--------|-------|
| **✅ Screening** | 30 min with recruiter (Thomas) | Background, motivation, process overview — **PASSED** |
| **R1** | 1 developer | Technical deep-dive — projects, Java, system thinking |
| **R2** | 2 developers | Live coding — read code, find bug, fix it |
| **R3** | Peer programming | Build/extend feature together with interviewer |
| **R4** | Closing | Culture fit, motivation, visa, compensation |

### What other candidates report online

Typical Picnic process (may vary by team/role):

1. HR / recruiter screening ✅ (you did this)
2. **Take-home assignment** (sometimes — you may or may not get one)
3. Technical discussion about assignment + experience
4. **Pair programming** with developers
5. Behavioural / closing round

> Oscar (Senior SWE, relocated from Australia): *"Interviewers seemed switched on, asked good questions, felt personal — not reading from a script."*  
> Source: [Relocate.me interview](https://relocate.me/blog/expat-stories/moving-to-the-netherlands-for-an-it-job-oscars-relocation-story/)

### Hiring Sprints (awareness only)
Picnic occasionally runs **"Hiring Sprints"** — all interviews in one day, offer within 24 hours. Your process is the standard multi-round path.

---

## 5. Round-by-Round Prep

### Round 1 — Technical Deep-Dive (1 developer)

**Duration:** ~45–60 min  
**Format:** Conversation + technical probing

**Prepare:**
| Topic | Your story |
|-------|------------|
| Walk me through your background | 2-min pitch (Red Hat → Vodafone) |
| Harbor architecture | Event-driven, Kafka, authoritative data source |
| Hardest technical challenge | Latency reduction, scale, failure handling |
| Why Kafka? | Decoupling, replay, multiple consumers |
| Database choice | PostgreSQL for structured; when MongoDB fits |
| Code quality | Code reviews, testing, CI/CD |

**Go 3 levels deep on any project:**
1. What did you build? (high level)
2. How did you build it? (architecture, tech choices)
3. What would you change? (trade-offs, lessons learned)

**Practice questions:**
- "How do you handle duplicate messages in Kafka?"
- "How do you ensure idempotency in order processing?"
- "Describe a production incident you debugged."

---

### Round 2 — Live Bug Fix (2 developers)

**Duration:** ~45–60 min  
**Format:** Given Java code with bugs → find and fix while explaining

**What they're testing:**
- Can you read unfamiliar code quickly?
- Do you spot common bugs (off-by-one, NPE, Optional misuse, boundaries)?
- Do you communicate while debugging?
- Do you consider edge cases (empty list, null input)?

**Prep:** See [PICNIC-INTERVIEW-PREP.md](../PICNIC-INTERVIEW-PREP.md) — daily bug-fix exercises.

**During the round:**
1. **Read first** — understand what the code should do
2. **Ask clarifying questions** — "Should free delivery include exactly €50?"
3. **Narrate** — "I'm checking the loop bounds because..."
4. **Fix one bug at a time** — don't change everything at once
5. **Mention improvements** — null checks, tests you'd add

---

### Round 3 — Peer Programming (2 developers)

**Duration:** ~60 min  
**Format:** Build or extend a feature together

**Likely tasks:**
- Add validation to a REST endpoint
- Implement a service method (`applyDiscount`, `filterInStock`)
- Write a unit test for existing code
- Extend a DTO + map to entity

**What they're watching:**
| Signal | Good | Bad |
|--------|------|-----|
| Communication | "I'll start with the service layer because..." | Silent coding |
| Collaboration | "What do you think about this approach?" | Ignoring interviewer input |
| Code quality | Clean naming, small methods | 100-line method |
| Testing mindset | "Should we add a test for the edge case?" | No mention of tests |

**Prep:** Practice coding out loud. Review Spring Controller → Service → Repository pattern in [JAVA-SPRING-REVISION.md](./JAVA-SPRING-REVISION.md).

---

### Round 4 — Closing Interview

**Duration:** ~30–45 min  
**Topics:**
- Why Picnic? Why Store? Why Netherlands?
- Visa / relocation timeline (60 days notice)
- Salary expectations (research: mid-level SWE Amsterdam ~€55K–75K base)
- Questions about team, onboarding, growth

**Why Picnic (your answer):**
> Picnic builds grocery delivery from scratch with serious engineering — routing, warehouse automation, consumer features at scale. The Store team owns features millions use daily. I want product-focused backend work in an international environment, and Amsterdam is where I want to grow.

**Questions to ask:**
1. What does the Store team own in the next 6 months?
2. How does Picnic support international relocation and visa sponsorship?
3. What does onboarding look like for backend engineers?
4. How do teams balance feature delivery vs technical debt?

---

## 6. Topics Likely to Come Up (Store + Picnic context)

### Grocery / e-commerce domain (know conceptually)
| Concept | Backend implication |
|---------|---------------------|
| Product catalog | CRUD, search, categorization, caching |
| Cart / checkout | Session state, consistency, payment integration |
| Inventory | Stock levels, reservation, race conditions |
| Orders | State machine: placed → picked → delivered |
| Personalization | Event history, recommendations |
| Loyalty | Points accrual, idempotent reward logic |

You don't need domain expertise — show you can **learn fast** and connect backend patterns to business problems.

### System design (light — R1 may touch this)
- How would you design a **meal recommendation** feature?
- How would you handle **peak load** during holiday shopping?
- **Cache** product catalog — Redis, TTL, invalidation

Keep answers practical: API → Service → DB → Cache → Events.

---

## 7. Behavioural (STAR Stories)

Prepare 3 stories:

| Story | Situation | Use for |
|-------|-----------|---------|
| **Harbor latency** | Reduced pipeline latency 30% | Technical challenge, ownership |
| **Vodafone migration** | 30M customers, 40+ workflows | Scale, complexity |
| **Production incident** | Debugged and fixed under pressure | Reliability, calm under stress |
| **Code review / disagreement** | Technical decision with team | Collaboration |

**STAR format:** Situation → Task → Action → Result (with numbers).

---

## 8. Visa & Relocation

| Item | Detail |
|------|--------|
| Visa type | Netherlands **Highly Skilled Migrant** (kennismigrant) |
| Who sponsors | Picnic (employer) |
| Your timeline | ~60 days notice at Red Hat |
| Language | English sufficient; Dutch not required |
| Office | Amsterdam, office-first with some WFH flexibility |

**If asked:** "I'm fully committed to relocating. I understand Picnic sponsors the work visa. I can join after approximately 60 days notice."

---

## 9. What NOT to Do

- Don't badmouth Red Hat or Vodafone
- Don't pretend to know Reactor/MongoDB deeply if you don't — say "I've used X, excited to learn Y"
- Don't negotiate salary aggressively in early rounds
- Don't say you're interviewing at 10 companies
- Don't treat it as LeetCode — they want **practical Java engineering**
- Don't code silently in pair programming — **talk constantly**

---

## 10. Study Plan (Linked to Your Roadmap)

| Daily | Activity | Doc |
|-------|----------|-----|
| 45 min | Hands-on bug fix / pair prog | [PICNIC-INTERVIEW-PREP.md](../PICNIC-INTERVIEW-PREP.md) |
| 30 min | Java/Spring revision (1 section/day) | [JAVA-SPRING-REVISION.md](./JAVA-SPRING-REVISION.md) |
| 30 min | Practice 2-min pitch + 1 STAR story out loud | This guide §5, §7 |
| 2 hrs | DSA (maintain pattern skills) | DSA roadmap |

### Before each round checklist
- [ ] **R1:** Architecture notes for Harbor + Vodafone printed/memorized
- [ ] **R2:** 3 bug-fix drills in last 48 hours
- [ ] **R3:** 1 pair-programming mock completed
- [ ] **R4:** Why Picnic answer + 3 questions ready

---

## 11. Useful Links

| Resource | URL |
|----------|-----|
| Picnic Tech Careers | https://jobs.picnic.app/en/tech |
| Picnic Blog (engineering culture) | https://blog.picnic.nl/ |
| Relocate.me — Picnic engineer story | https://relocate.me/blog/expat-stories/moving-to-the-netherlands-for-an-it-job-oscars-relocation-story/ |
| Application Tracker | [APPLICATION-TRACKER.md](../APPLICATION-TRACKER.md) |
| Hands-on exercises | [PICNIC-INTERVIEW-PREP.md](../PICNIC-INTERVIEW-PREP.md) |
| Java/Spring revision | [JAVA-SPRING-REVISION.md](./JAVA-SPRING-REVISION.md) |

---

## 12. Quick Reference Card (Print This)

```
PICNIC — SOFTWARE ENGINEER (STORE)
─────────────────────────────────
Team:     Consumer domain — Meal Planner, loyalty, personalization
Stack:    Java 21, Spring Boot 3, Kafka, PostgreSQL, MongoDB, K8s
Rounds:   R1 deep-dive → R2 bug fix → R3 pair prog → R4 closing

YOUR EDGE:
  • 5 YoE Java/Spring/Kafka — matches their band
  • Harbor: event-driven, production scale
  • Vodafone: 30M users, complex workflows
  • Open source: Apache Commons

YOUR PITCH (30 sec):
  "Backend engineer at Red Hat building event-driven data platforms.
   Before that Vodafone at 30M-user scale. I want consumer-facing
   backend work at Picnic's Store team in Amsterdam."

REMEMBER:
  • Talk while coding
  • Ask clarifying questions
  • Product mindset > pure algorithms
  • They want engineers who OWN outcomes
```
