```mermaid
flowchart TB
   Client[Client Application]
   API[API Layer]
   EventBus[ Event Bus]
   MongoDB[(EventStore-MongoDB)]
   ReadDB[(Read Database)]

   subgraph Command Side
       direction TB
       API --> |Commands| EventBus
       EventBus--> |Events| MongoDB
       MongoDB-->|Project Events| ReadDB
   end

   subgraph Query Side
        direction TB
        ReadAPI[Read API]
        ReadDB-->|Query Results| ReadAPI
   end

   Client -->|Write Operations| API
   Client -->|Read Operations| ReadAPI
   


```
