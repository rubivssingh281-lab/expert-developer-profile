# Martin Fowler's Patterns of Enterprise Application Architecture (PoEAA)

Synthesized from **Martin Fowler's Catalog of Enterprise Application Architecture (PoEAA)**.

---

## 1. Domain Logic Patterns

### Domain Model vs. Transaction Script
- **Transaction Script**: Organizes business logic by procedures where each procedure handles a single request from the presentation.
  * *When to use*: Simple CRUD applications with little business logic.
- **Domain Model**: An object model of the domain that incorporates both behavior and data. Rich entity models enforce invariants internally.
  * *When to use*: Complex, evolving business rules, state machines, validation rules.
- **Service Layer**:
  * Defines an application's boundary with a layer of services that establishes a set of available operations and coordinates the application's response in each operation.
  * The Service Layer encapsulates domain transactions and orchestrates atomic business operations across multiple repositories.

---

## 2. Object-Relational Behavioral Patterns

### Unit of Work
Maintains a list of objects affected by a business transaction and coordinates the writing out of changes and the resolution of concurrency problems.
- Tracks dirty, new, and deleted entities in memory during the transaction scope.
- In SQLAlchemy: The `AsyncSession` implements the Unit of Work pattern natively. Group operations inside an async context:
```python
async with async_session_factory() as session:
    async with session.begin():
        user = await repo_user.get(session, user_id)
        user.upgrade_tier()
        order = Order(user_id=user.id, amount=99.0)
        session.add(order)
    # Unit of Work issues optimal batch SQL INSERT/UPDATE and commits atomically
```

### Identity Map
Ensures that each object gets loaded only once by keeping every loaded object in a map. Looks up objects using the map when referring to them.
- Prevents database load and guarantees object identity consistency within a single transaction session.

---

## 3. Data Source & Distribution Patterns

### Repository vs. Data Mapper
- **Data Mapper**: A layer of Mappers that moves data between objects and a database while keeping them independent of each other and the mapper itself.
- **Repository**: Mediates between the domain and data mapping layers using a collection-like interface for accessing domain objects (`find_by_id`, `add`, `remove`, `list_active`).

### Data Transfer Object (DTO)
An object that carries data between processes in order to reduce the number of method calls and prevent exposure of internal domain structures.
- In FastAPI: Pydantic schemas (`OrderCreateRequest`, `OrderResponse`) are the formal realization of Fowler's DTO pattern.

---

## 4. Offline Concurrency Patterns for Long-Running Transactions

In enterprise systems, business transactions often span multiple HTTP requests (e.g., a wizard workflow or multi-step checkout). Holding database transaction locks open across HTTP requests is an anti-pattern. Fowler defines two primary solutions:

### Optimistic Offline Lock
- **Assumption**: Concurrent conflict is infrequent.
- **Mechanism**: Multiple users view and edit records concurrently without blocking. A version number or timestamp is verified during the commit phase:
```sql
UPDATE orders 
SET status = 'SHIPPED', version_id = version_id + 1
WHERE id = :id AND version_id = :expected_version;
```
- **Trade-off**: Maximum concurrency and throughput; however, if two users submit simultaneously, the second user's update is rejected and must be retried or resolved.

### Pessimistic Offline Lock
- **Assumption**: Probability of concurrent conflict is high, and the cost of having a user's work rejected at the end is unacceptable.
- **Mechanism**: A business transaction must acquire an exclusive lock record (or distributed Redis key with lease TTL) *before* editing begins. All other sessions are barred from modifying the resource until the lease is released or expires.
- **Trade-off**: Guarantees updates will never clash at commit time; however, reduces system concurrency and requires strict lease timeout monitoring to avoid abandoned locks.

### Value Object (VO)
A small simple object, like money or a date range, whose equality isn't based on identity, but rather on value.
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    amount: float
    currency: str

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
        return Money(self.amount + other.amount, self.currency)
```
