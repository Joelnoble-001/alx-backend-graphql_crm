from datetime import datetime
import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    # Optional: verify GraphQL hello field
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

    # Append to log
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(message)
