MongoDB Atlas provides robust support for federated queries through its **Atlas Data Federation** feature. 
Here are some key aspects of federated query support:

### **Supported Data Sources:**
- **Atlas Clusters**: We can query data stored in your MongoDB Atlas clusters.
- **AWS S3 Buckets**: Query data stored in S3 buckets.
- **Azure Blob Storage**: Query data stored in Azure Blob Storage containers.
- **HTTP/HTTPS URLs**: Query data hosted at publicly accessible URLs.
- **Online Archives**: Query archived data stored in Atlas Online Archives.

### **Query Capabilities:**
- **MongoDB Query Language (MQL)**: We can use MQL to run queries against federated data.
- **Aggregation Pipeline**: Supports most standard server commands and stages in the aggregation pipeline.
- **Virtual Databases and Collections**: Atlas Data Federation creates virtual databases and collections based on your configuration.

### **Configuration and Management:**
- **Storage Configuration**: Define thr federated database instance store and map virtual databases and collections to the data sources.
- **Query Limits**: Optionally configure limits on the amount of data processed for queries to control costs.
- **Roles and Permissions**: A database user must have appropriate roles (e.g., `readWriteAnyDatabase`, `readAnyDatabase`, or a custom role with the `find` privilege) to run queries against a federated database instance.

### **Limitations:**
- **Field Order Sensitivity**: Atlas Data Federation doesn't support queries that are field-order sensitive, such as embedded document equality queries or sorting on a document field.
- **Cross-Cloud Queries**: Federated queries cannot span across different cloud providers (e.g., querying data in both AWS S3 and Azure Blob Storage simultaneously).

### **Use Cases:**
- **Data Integration**: Seamlessly query, transform, and aggregate data from multiple sources.
- **Data Migration**: Move data between different storage formats (e.g., from S3 to Atlas clusters).
- **Analytics**: Derive insights from data stored in various formats without needing to move it.

