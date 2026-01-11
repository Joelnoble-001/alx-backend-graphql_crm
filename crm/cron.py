from datetime import datetime
import requests

def log_crm_heartbeat():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    # Optional: verify GraphQL endpoint is responsive
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=5
        )
        if response.status_code != 200:
            message = f"{timestamp} CRM is alive (GraphQL unreachable)\n"
    except Exception:
        message = f"{timestamp} CRM is alive (GraphQL error)\n"

    with open("/tmp/crm_heartbeat_log.txt", "a") as file:
        file.write(message)
