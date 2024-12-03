Certainly! Here are more detailed examples and guidance on how to integrate Azure API Management (APIM) with Event Hubs and Event Grid, along with scenarios for direct communication with Event Hubs/Event Grid.

1. Scenario 1: Using API Management to Expose APIs that Interact with Event Hubs

In this scenario, we’ll expose a simple REST API via API Management that receives events from external systems (e.g., Salesforce, ReactJS, Node.js), transforms them, and forwards them to Event Hubs for further processing.

Step 1: Create an API in Azure API Management

1. Go to your API Management instance in the Azure portal.


2. Click on APIs under the API Management service.


3. Select Add API and choose HTTP as the API type.


4. Define the API by specifying:

Name: EventIngestionAPI

API URL: /events

Request type: POST


This API will accept JSON payloads containing event data.



Step 2: Define the API Operation

Create an operation that receives event data and forwards it to Event Hubs.

1. Under the API you just created, click on Design and add a POST operation.


2. Define the Request schema for the expected event data.



{
  "type": "object",
  "properties": {
    "eventType": { "type": "string" },
    "data": {
      "type": "object",
      "properties": {
        "orderId": { "type": "string" },
        "customer": { "type": "string" }
      }
    }
  }
}

Step 3: Set Up API Policies

Now, we need to create a policy to transform the incoming request (e.g., modify the format) and send it to Event Hubs.

1. Click on the Design tab of the API and select the Inbound Processing section.


2. Add the following policy to forward the event to Event Hubs using the Azure Event Hubs SDK:



<inbound>
  <base />
  <set-variable name="eventBody" value="@(context.Request.Body.As<JObject>())" />
  <send-request mode="new" response-variable-name="eventHubResponse">
    <set-url>https://<event-hubs-namespace>.servicebus.windows.net/<event-hub-name>/messages</set-url>
    <set-method>POST</set-method>
    <set-body>@(eventBody)</set-body>
    <set-header name="Content-Type" exists-action="override">
      <value>application/json</value>
    </set-header>
    <set-header name="Authorization" exists-action="override">
      <value>@(context.Variables["EventHubToken"])</value>
    </set-header>
  </send-request>
</inbound>

This policy:

Extracts the request body as the event data.

Sends the event to Event Hubs via an HTTP POST request.

Includes the Authorization header for Event Hubs using the previously acquired Event Hub SAS token.


Step 4: Handle Event in Event Hubs

Once the event is received by Event Hubs, you can process it using Azure Functions, Stream Analytics, or other Azure services that can consume events from Event Hubs.

For example, using an Azure Function:

1. Create a function with a trigger for Event Hubs.


2. In the function code, process the incoming event (store it in Azure SQL Database, Cosmos DB, etc.).



[FunctionName("ProcessEventHubEvent")]
public static async Task Run(
    [EventHubTrigger("eventHubName", Connection = "EventHubConnectionString")] string myEvent,
    ILogger log)
{
    log.LogInformation($"Received event: {myEvent}");
    // Process event (store in database, etc.)
}

Step 5: Expose a Response (Optional)

You can return a response to the caller to confirm that the event was successfully ingested.

<outbound>
  <base />
  <set-body>@{{
    return "Event successfully ingested to Event Hubs.";
  }}</set-body>
</outbound>


---

2. Scenario 2: Using Event Grid to Route Events to Multiple Systems

In this scenario, we use Event Grid to route events from Event Hubs to downstream systems (e.g., other APIs, microservices, or Azure functions).

Step 1: Create Event Grid Topic

1. Go to the Azure portal and search for Event Grid Topics.


2. Click on + Create and follow the wizard to create a new Event Grid Topic.

Give it a name like SalesforceEventsTopic.




Step 2: Create Event Grid Subscription

Now, create a subscription that will route the events to an API endpoint exposed by API Management.

1. Go to the Event Grid Topic you created.


2. Under Event Subscriptions, click + Event Subscription.


3. Define the destination (for example, a Webhook that is an API exposed through API Management).


4. In Endpoint Type, select Webhook and set the URL to the API Management endpoint (e.g., https://<apim-instance>.azure-api.net/api/receiveEvent).



Step 3: Send Events to Event Grid

You can now send events from Event Hubs to Event Grid. You can set up an Azure Function to consume events from Event Hubs and publish them to Event Grid.

Here’s an example of an Azure Function that listens to Event Hubs and sends the event to Event Grid:

[FunctionName("SendEventToEventGrid")]
public static async Task Run(
    [EventHubTrigger("eventHubName", Connection = "EventHubConnectionString")] string myEvent,
    [EventGrid(TopicEndpointUri = "EventGridTopicUri", TopicKey = "EventGridTopicKey")] IAsyncCollector<EventGridEvent> outputEvents,
    ILogger log)
{
    var eventGridEvent = new EventGridEvent
    {
        Id = Guid.NewGuid().ToString(),
        EventTime = DateTime.UtcNow,
        EventType = "Salesforce.OrderCreated",
        Subject = "orders/12345",
        Data = new { orderId = "12345", customer = "John Doe" }
    };

    await outputEvents.AddAsync(eventGridEvent);
    log.LogInformation($"Event sent to Event Grid: {eventGridEvent.Id}");
}

Step 4: Process Events in the Subscriber API

Once the event is published to Event Grid, it will trigger the subscribed endpoint (the API exposed by API Management) to process the event.

For example, the API can respond by updating records, triggering workflows, or notifying users.


---

3. Scenario 3: Direct Integration with Event Hubs (No API Management)

If you don’t need API Management, you can directly send events to Event Hubs from external systems like Salesforce, ReactJS, or Node.js applications.

Direct Integration Example with Node.js:

Here’s a simple Node.js example of sending an event to Event Hubs directly using the Azure Event Hubs SDK:

const { EventHubProducerClient } = require("@azure/event-hubs");

const producer = new EventHubProducerClient("<event-hubs-connection-string>", "<event-hub-name>");

async function sendEvent() {
  const eventData = {
    eventType: "Salesforce.OrderCreated",
    data: {
      orderId: "12345",
      customer: "John Doe"
    }
  };

  const batch = await producer.createBatch();
  batch.tryAdd(eventData);

  await producer.sendBatch(batch);
  console.log("Event sent to Event Hubs.");
}

sendEvent().catch((err) => {
  console.error("Error occurred: ", err);
});

Direct Integration Example with Event Grid:

For Event Grid, you can directly publish events using the Event Grid REST API from your application. Here’s an example in Node.js:

const axios = require("axios");

const eventGridEndpoint = "<event-grid-topic-url>";
const topicKey = "<event-grid-topic-key>";

const event = {
  id: "12345",
  eventType: "Salesforce.OrderCreated",
  subject: "orders/12345",
  data: {
    orderId: "12345",
    customer: "John Doe"
  },
  eventTime: new Date().toISOString(),
  dataVersion: "1.0"
};

axios.post(eventGridEndpoint, [event], {
  headers: {
    "aeg-sas-key": topicKey,
    "Content-Type": "application/json"
  }
})
.then(() => console.log("Event sent to Event Grid"))
.catch((error) => console.error("Error occurred: ", error));


---

4. Conclusion

API Management adds value if you need to expose secure, monitored APIs to external systems, manage event transformations, enforce security policies, and log API usage.

Event Hubs/Event Grid provide the backbone for handling and routing events. You can directly integrate with them, but if you want to enforce additional layers like security, logging, or API transformation, **API Management


