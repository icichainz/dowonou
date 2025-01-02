from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.db.models import F
from django.conf import settings
from .models import Rental, Tool, Notification, User
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_rental_reminder():
    """
    Send reminders for upcoming rentals to both renters and tool owners.
    """
    tomorrow = timezone.now() + timezone.timedelta(days=1)
    upcoming_rentals = Rental.objects.filter(
        start_date__date=tomorrow.date(), status="approved"
    )

    for rental in upcoming_rentals:
        # Reminder to renter
        send_mail(
            "Rental Reminder",
            f"Your rental of {rental.tool.name} is scheduled to start tomorrow.",
            settings.DEFAULT_FROM_EMAIL,
            [rental.renter.email],
            fail_silently=False,
        )

        # Reminder to tool owner
        send_mail(
            "Rental Reminder",
            f"Your tool {rental.tool.name} is scheduled for rental starting tomorrow.",
            settings.DEFAULT_FROM_EMAIL,
            [rental.tool.owner.email],
            fail_silently=False,
        )

    logger.info(f"Sent reminders for {upcoming_rentals.count()} upcoming rentals.")


@shared_task
def update_tool_availability():
    """
    Update tool availability based on current rentals.
    """
    current_time = timezone.now()

    # Mark tools as unavailable for ongoing rentals
    Rental.objects.filter(
        start_date__lte=current_time, end_date__gte=current_time, status="approved"
    ).update(tool__availability=False)

    # Mark tools as available after rental period
    Rental.objects.filter(end_date__lt=current_time, status="approved").update(
        tool__availability=True
    )

    logger.info("Updated tool availability based on current rentals.")


@shared_task
def process_rental_completion():
    """
    Process completed rentals, update status, and send notifications.
    """
    completed_rentals = Rental.objects.filter(
        end_date__lt=timezone.now(), status="approved"
    )

    for rental in completed_rentals:
        rental.status = "completed"
        rental.save()

        # Notification for renter
        Notification.objects.create(
            user=rental.renter,
            message=f"Your rental of {rental.tool.name} has been completed. Please leave a review.",
        )

        # Notification for tool owner
        Notification.objects.create(
            user=rental.tool.owner,
            message=f"The rental of your tool {rental.tool.name} has been completed.",
        )

    logger.info(f"Processed {completed_rentals.count()} completed rentals.")


@shared_task
def calculate_earnings():
    """
    Calculate and update earnings for tool owners.
    """
    completed_rentals = Rental.objects.filter(
        status="completed", earnings_processed=False
    )

    for rental in completed_rentals:
        owner = rental.tool.owner
        owner.total_earnings = F("total_earnings") + rental.total_cost
        owner.save()

        rental.earnings_processed = True
        rental.save()

    logger.info(
        f"Calculated earnings for {completed_rentals.count()} completed rentals."
    )


@shared_task
def send_inactive_user_reminder():
    """
    Send reminders to users who haven't logged in for a while.
    """
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=thirty_days_ago)

    for user in inactive_users:
        send_mail(
            "We miss you!",
            "It's been a while since you last visited our tool rental platform. Check out our latest tools!",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

    logger.info(f"Sent reminders to {inactive_users.count()} inactive users.")


@shared_task
def clean_expired_notifications():
    """
    Remove notifications older than 30 days.
    """
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    deleted_count, _ = Notification.objects.filter(
        created_at__lt=thirty_days_ago
    ).delete()
    logger.info(f"Cleaned {deleted_count} expired notifications.")


@shared_task
def update_tool_rankings():
    """
    Update tool rankings based on rental frequency and ratings.
    """
    from django.db.models import Count, Avg

    tools = Tool.objects.annotate(
        rental_count=Count("rental"), avg_rating=Avg("rental__review__rating")
    )

    for tool in tools:
        # This is a simplified ranking algorithm. In a real-world scenario,
        # you might want to use a more sophisticated approach.
        tool.ranking = (tool.rental_count * 0.7) + (tool.avg_rating or 0 * 0.3)
        tool.save()

    logger.info("Updated rankings for all tools.")


@shared_task
def generate_monthly_report():
    """
    Generate and email monthly report to admins.
    """
    from django.db.models import Sum, Count
    from io import StringIO
    import csv

    # Generate report data
    total_rentals = Rental.objects.filter(
        created_at__gte=timezone.now() - timezone.timedelta(days=30)
    ).count()
    total_revenue = (
        Rental.objects.filter(status="completed").aggregate(Sum("total_cost"))[
            "total_cost__sum"
        ]
        or 0
    )
    new_users = User.objects.filter(
        date_joined__gte=timezone.now() - timezone.timedelta(days=30)
    ).count()

    # Create CSV file
    csv_file = StringIO()
    writer = csv.writer(csv_file)
    writer.writerow(["Metric", "Value"])
    writer.writerow(["Total Rentals", total_rentals])
    writer.writerow(["Total Revenue", total_revenue])
    writer.writerow(["New Users", new_users])

    # Email report to admins
    send_mail(
        "Monthly Rental Platform Report",
        "Please find attached the monthly report for the tool rental platform.",
        settings.DEFAULT_FROM_EMAIL,
        [admin[1] for admin in settings.ADMINS],
        fail_silently=False,
        attachments=[("monthly_report.csv", csv_file.getvalue(), "text/csv")],
    )

    logger.info("Generated and sent monthly report to admins.")
