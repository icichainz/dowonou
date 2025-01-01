from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'send-rental-reminders': {
        'task': 'rental_platform.tasks.send_rental_reminder',
        'schedule': crontab(hour=9, minute=0),  # Run daily at 9 AM
    },
    'update-tool-availability': {
        'task': 'rental_platform.tasks.update_tool_availability',
        'schedule': crontab(minute='*/15'),  # Run every 15 minutes
    },
    'process-rental-completion': {
        'task': 'rental_platform.tasks.process_rental_completion',
        'schedule': crontab(hour='*/1'),  # Run every hour
    },
    'calculate-earnings': {
        'task': 'rental_platform.tasks.calculate_earnings',
        'schedule': crontab(hour=0, minute=0),  # Run daily at midnight
    },
    'send-inactive-user-reminder': {
        'task': 'rental_platform.tasks.send_inactive_user_reminder',
        'schedule': crontab(day_of_week=1, hour=10, minute=0),  # Run weekly on Monday at 10 AM
    },
    'clean-expired-notifications': {
        'task': 'rental_platform.tasks.clean_expired_notifications',
        'schedule': crontab(hour=1, minute=0),  # Run daily at 1 AM
    },
    'update-tool-rankings': {
        'task': 'rental_platform.tasks.update_tool_rankings',
        'schedule': crontab(hour='*/6'),  # Run every 6 hours
    },
    'generate-monthly-report': {
        'task': 'rental_platform.tasks.generate_monthly_report',
        'schedule': crontab(day_of_month=1, hour=2, minute=0),  # Run on the 1st of each month at 2 AM
    },
}
