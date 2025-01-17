
```mermaid
flowchart TD
    subgraph Application
        A[Spring Boot Application] --> B[Command Handler]
        B --> C[Event Store (MongoDB)]
        B --> D[Message Broker (Kafka)]
    end

    subgraph EventStore
        C --> E[Event Stream]
    end

    subgraph MessageBroker
        D --> F[Kafka Topic]
    end

    subgraph Consumers
        F --> G[Event Processor]
        G --> H[Read Model Updater]
        H --> I[Read Model (MongoDB)]
    end

    style Application fill:#f9f,stroke:#333,stroke-width:4px
    style EventStore fill:#bbf,stroke:#333,stroke-width:4px
    style MessageBroker fill:#bfb,stroke:#333,stroke-width:4px
    style Consumers fill:#ffb,stroke:#333,stroke-width:4px
```
