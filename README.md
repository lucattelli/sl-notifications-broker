# Notifications Broker for the game Second Life

I've written this service that sends in-game notifications to Second Life users. It uses DDD to model the notification lifecycle, as well as the notification queue. It uses Hexagonal to properly decouple the domain model from infrastructure (like the REST API, the database service used and the integration with the notification workers).

## Architecture

### Domain and Application Layers

These are responsible for managing application-independent business rules (aka: domain entities, domain services) and application-dependent business rules (aka application services and use cases). Those should be enough  to guarantee the whole notification lifecycle.

### Infrastructure Layer

Here we have a REST API for other services to create and check on notifications. If you're using an event-driven architecture (I personally prefer this as well), you can implement your event handlers here to generate notifications according to relevant events in your application.

We also have the integration with the database. It's currently using Mongo, but you could actually use any database you want. Just implement the adapters based on the repository ports and you're good.

We also have the Second Life notification worker. This is written in Linden Scripting Language. When added to an in-game object, this script will register itself as a worker and will periodically check via REST API for new notifications sitting in the queue to be sent. It also exposes a Second Life URL that can be used to force a immediate check.

We're also using Celery as a task runner to process the notification after its created/updated via REST API. This ensures our API is fast, with as little I/O blocking as possible, while still ensuring the API client that a notification will either be sent immediately (if any worker responds to a call to its Second Life URL) or later by adding it to the queue.

We also use Celery Beat to check on notifications sitting in the queue for too long, lost workers, etc.

