"""
Celery configuration for Power Quality Analyzer project.
"""

import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'power_quality_core.settings.development')

app = Celery('power_quality')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Configure periodic tasks
app.conf.beat_schedule = {
    'process-raw-signals': {
        'task': 'apps.signal_acquisition.tasks.process_raw_signals',
        'schedule': 1.0,  # every second
    },
    'calculate-power-metrics': {
        'task': 'apps.power_metrics.tasks.calculate_power_metrics',
        'schedule': 5.0,  # every 5 seconds
    },
    'analyze-harmonics': {
        'task': 'apps.harmonic_analysis.tasks.analyze_harmonics',
        'schedule': 10.0,  # every 10 seconds
    },
    'check-device-status': {
        'task': 'apps.device_management.tasks.check_device_status',
        'schedule': 30.0,  # every 30 seconds
    },
    'generate-daily-report': {
        'task': 'apps.historical_analysis.tasks.generate_daily_report',
        'schedule': crontab(minute=0, hour=0),  # midnight
    },
    'cleanup-old-data': {
        'task': 'apps.historical_analysis.tasks.cleanup_old_data',
        'schedule': crontab(minute=0, hour=1),  # 1 AM
    },
}

# Task routing
app.conf.task_routes = {
    'apps.signal_acquisition.*': {'queue': 'signal_processing'},
    'apps.harmonic_analysis.*': {'queue': 'analysis'},
    'apps.power_metrics.*': {'queue': 'metrics'},
    'apps.historical_analysis.*': {'queue': 'reporting'},
    'apps.alerts_notifications.*': {'queue': 'notifications'},
}

# Task settings
app.conf.task_time_limit = 30  # seconds
app.conf.task_soft_time_limit = 25
app.conf.worker_prefetch_multiplier = 1
app.conf.task_acks_late = True

@app.task(bind=True)
def debug_task(self):
    """Task for debugging purposes."""
    print(f'Request: {self.request!r}') 