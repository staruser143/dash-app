```mermaid
flowchart TD
        A[Spring Boot Application] --> B[Command Handler]
        B --> C[Event Store (MongoDB)]
        B --> D[Message Broker (Kafka)]
    end
```
