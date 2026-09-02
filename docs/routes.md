# RESTful Routes — Aquaflow Tracker
> Response shape: { "status": int, "data": {...}, "error": null }

## Customers
| Method | Path | Handler | Status | Example Response |
|---|---|---|---|---|
| GET | /customers | listCustomers | 200 | {"status":200,"data":{"message":"listCustomers stub"},"error":null} |
| GET | /customers/:customer_id | showCustomer | 200 | {"status":200,"data":{"message":"showCustomer stub","customer_id":"C001"},"error":null} |
| POST | /customers | createCustomer | 201 | {"status":201,"data":{"message":"createCustomer stub"},"error":null} |
| PUT | /customers/:customer_id | updateCustomer | 200 | {"status":200,"data":{"message":"updateCustomer stub","customer_id":"C001"},"error":null} |
| DELETE | /customers/:customer_id | deleteCustomer | 200 | {"status":200,"data":{"message":"deleteCustomer stub","customer_id":"C001"},"error":null} |

## Products
| Method | Path | Handler | Status | Example Response |
|---|---|---|---|---|
| GET | /products | listProducts | 200 | {"status":200,"data":{"message":"listProducts stub"},"error":null} |
| GET | /products/:product_id | showProduct | 200 | {"status":200,"data":{"message":"showProduct stub","product_id":"P002"},"error":null} |
| POST | /products | createProduct | 201 | {"status":201,"data":{"message":"createProduct stub"},"error":null} |
| PUT | /products/:product_id | updateProduct | 200 | {"status":200,"data":{"message":"updateProduct stub","product_id":"P002"},"error":null} |
| DELETE | /products/:product_id | deleteProduct | 200 | {"status":200,"data":{"message":"deleteProduct stub","product_id":"P002"},"error":null} |

## Orders
| Method | Path | Handler | Status | Example Response |
|---|---|---|---|---|
| GET | /orders | listOrders | 200 | {"status":200,"data":{"message":"listOrders stub"},"error":null} |
| GET | /orders/:order_id | showOrder | 200 | {"status":200,"data":{"message":"showOrder stub","order_id":"O005"},"error":null} |
| POST | /orders | createOrder | 201 | {"status":201,"data":{"message":"createOrder stub"},"error":null} |
| PUT | /orders/:order_id | updateOrder | 200 | {"status":200,"data":{"message":"updateOrder stub","order_id":"O005"},"error":null} |
| DELETE | /orders/:order_id | deleteOrder | 200 | {"status":200,"data":{"message":"deleteOrder stub","order_id":"O005"},"error":null} |

## Collections
| Method | Path | Handler | Status | Example Response |
|---|---|---|---|---|
| GET | /collections | listCollections | 200 | {"status":200,"data":{"message":"listCollections stub"},"error":null} |
| GET | /collections/:collection_id | showCollection | 200 | {"status":200,"data":{"message":"showCollection stub","collection_id":"CL003"},"error":null} |
| POST | /collections | createCollection | 201 | {"status":201,"data":{"message":"createCollection stub"},"error":null} |
| PUT | /collections/:collection_id | updateCollection | 200 | {"status":200,"data":{"message":"updateCollection stub","collection_id":"CL003"},"error":null} |
| DELETE | /collections/:collection_id | deleteCollection | 200 | {"status":200,"data":{"message":"deleteCollection stub","collection_id":"CL003"},"error":null} |
