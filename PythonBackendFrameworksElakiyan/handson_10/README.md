# Course Management - Microservices Decomposition

## Task 1: Bounded Contexts

| Service Name | Responsibility | Endpoints it owns | Database it owns |
| :--- | :--- | :--- | :--- |
| Course Service | Department & course CRUD | `/api/courses/`, `/api/courses/<id>/` | `course_service.db` (own SQLite) |
| Student Service | Student CRUD, enrollment | `/api/students/`, `/api/students/<id>/enroll` | `student_service.db` (own SQLite) |
| Auth Service | Registration, login, token validation | `/api/auth/register/`, `/api/auth/login/` | `auth_service.db` (not built in this exercise - see Hands-On 9 for the JWT logic this would reuse) |
| Notification Service | Email/SMS confirmations | internal only, triggered by events | none (stateless) |

This exercise implements **Course Service** and **Student Service** as two
independent Flask apps (step 98), each with its own SQLite database, plus a
**Gateway** that routes between them.

## Task 2: Synchronous vs Asynchronous Inter-Service Communication

**Synchronous (HTTP, what we built here):** Student Service calls Course
Service directly over HTTP and waits for the response before continuing.
Simple to reason about and debug - it's just a function call over the
network. The cost is tight coupling: if Course Service is slow or down,
the enrollment request hangs or fails (we return 503 in that case). Latency
also stacks - every hop adds wait time.

**Asynchronous (message queue - RabbitMQ/Kafka):** Student Service would
publish an "EnrollmentRequested" event and return immediately; Course
Service (or a worker) consumes it later and reacts. This decouples the
two services - Course Service being down just delays processing, it
doesn't fail the request. The cost is eventual consistency: the student
doesn't get an immediate yes/no, and you need to handle out-of-order or
duplicate events.

**When to use a queue instead:** when the calling service doesn't need an
immediate answer (e.g. "send a confirmation email"), when you want to
buffer load spikes, or when you have many consumers reacting to one event.
For "is this course valid right now" - a value the caller needs before
continuing - synchronous is the right call here.

Note: a production API Gateway also handles auth, rate limiting, and SSL
termination. The `gateway/app.py` here only demonstrates the routing
concept, not those production concerns.
