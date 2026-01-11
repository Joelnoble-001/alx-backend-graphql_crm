#!/usr/bin/env python3

from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL endpoint
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# Calculate date range (last 7 days)
seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

query = gql("""
query ($startDate: Date!) {
  orders(orderDate_Gte: $startDate) {
    id
    customer {
      email
    }
  }
}
""")

result = client.execute(query, variable_values={"startDate": seven_days_ago})

# Log reminders
log_file = "/tmp/order_reminders_log.txt"
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(log_file, "a") as f:
    for order in result.get("orders", []):
        f.write(
            f"{timestamp} - Order ID: {order['id']}, "
            f"Customer Email: {order['customer']['email']}\n"
        )

print("Order reminders processed!")
