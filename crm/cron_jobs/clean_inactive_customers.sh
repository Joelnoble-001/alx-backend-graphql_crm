#!/bin/bash

# Navigate to project root (adjust if needed)
PROJECT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

# Run Django cleanup command
DELETED_COUNT=$(python3 "$PROJECT_DIR/manage.py" shell -c "
from django.utils import timezone
from datetime import timedelta
from customers.models import Customer
from orders.models import Order

one_year_ago = timezone.now() - timedelta(days=365)

inactive_customers = Customer.objects.exclude(
    id__in=Order.objects.filter(created_at__gte=one_year_ago).values_list('customer_id', flat=True)
)

count = inactive_customers.count()
inactive_customers.delete()
print(count)
")

# Log result with timestamp
echo \"$(date '+%Y-%m-%d %H:%M:%S') - Deleted customers: $DELETED_COUNT\" >> /tmp/customer_cleanup_log.txt
