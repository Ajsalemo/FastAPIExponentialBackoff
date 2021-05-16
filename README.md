# FastAPIExponentialBackoff
Trying out Fast API to implement exponential backoff when connecting to a MySQL instance

<br>

## Overview
A CRUD based REST API that connects to an Azure Database for MySQL instance. The idea behind this was to implement exponential backoffs/retries on non-programming related exceptions (ex. Operational errors) in a basic implementation.

### Endpoints
- `"/"` - GET request. Root path.
- `"/api/book/find/all"` - GE request. Finds all records.
- `"/api/book/find/{id}"` - GET request. Accepts an integer to look up its associated record.
- `"/api/book/add"` - POST request. Accepts a request body in JSON format to add a new record.
- `"/api/book/delete/{id}"` - DELETE request. Accepts an integer to look up and delete its associated record.
- `"/api/book/update/{id}"` - PUT request. Accepts an integer to look up and update its associated record.
