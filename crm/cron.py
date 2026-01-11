from datetime import datetime
import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# ------------------
# Heartbeat logger (every 5 minutes)
# ------------------
def log_crm_heartbeat():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    # Optional: check GraphQL hello field
    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=True,
            retries=1
        )
        client = Client(transport=transport, fetch_schema_from_transport=False)
        query = gql("{ hello }")
        result = client.execute(query)
        if "hello" not in result:
            message = f"{timestamp} CRM is alive (GraphQL did not respond)\n"
    except Exception:
        message = f"{timestamp} CRM is alive (GraphQL error)\n"

    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(message)


# ------------------
# Order reminders (Task 1, optional reuse)
# ------------------
def send_order_reminders():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql("""
    query {
      orders(orderDate_Gte: "%s") {
        id
        customer {
          email
        }
      }
    }
    """ % ((datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")))

    try:
        result = client.execute(query)
        orders = result.get("orders", [])

        with open("/tmp/order_reminders_log.txt", "a") as f:
            for order in orders:
                f.write(f"{timestamp} - Order ID: {order['id']}, Customer Email: {order['customer']['email']}\n")

        print("Order reminders processed!")

    except Exception as e:
        with open("/tmp/order_reminders_log.txt", "a") as f:
            f.write(f"{timestamp} - Error sending reminders: {str(e)}\n")


# ------------------
# Low stock updater (Task 3, every 12 hours)
# ------------------
def update_low_stock():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    mutation = gql("""
    mutation {
      updateLowStockProducts {
        updatedProducts {
          name
          stock
        }
        message
      }
    }
    """)

    try:
        result = client.execute(mutation)
        updates = result['updateLowStockProducts']['updatedProducts']

        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            for product in updates:
                f.write(f"{timestamp} - {product['name']}: {product['stock']}\n")

    except Exception as e:
        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            f.write(f"{timestamp} - Error updating low stock: {str(e)}\n")
