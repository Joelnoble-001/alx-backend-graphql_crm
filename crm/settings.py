# crm/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',
    'crm',
]

# Cron job configuration
CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'), # heartbeat every 5 minutes
    ('0 */12 * * *', 'crm.cron.update_low_stock'), # low stock updater every 12 hours
]

# Other minimal Django settings needed to avoid errors
SECRET_KEY = 'replace-this-with-any-string'
DEBUG = True
ALLOWED_HOSTS = []
ROOT_URLCONF = 'crm.urls'
WSGI_APPLICATION = 'crm.wsgi.application'
