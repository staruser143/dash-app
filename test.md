```mermaid
flowchart TB
    c1-->a2
    subgraph one
    a1-->a2
    end
    subgraph two
    b1-->b2
    end
    subgraph three
    c1-->c2
    end
    one --> two
    three --> two
    two --> c2
```
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
```
