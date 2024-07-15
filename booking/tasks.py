from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Reservation
from django.contrib.auth.models import User

@shared_task
def send_welcome_email(user_id):
    """
    Send a welcome email to the newly registered user.
    """
    user = User.objects.get(id=user_id)
    send_mail(
        subject='Welcome to Our Theater Ticketing System',
        message=f'Hello {user.username},\n\nWelcome to our theater ticketing system. We are excited to have you with us!',
        from_email='noreply@theater.com',
        recipient_list=[user.email],
    )
    return f'Sent welcome email to {user.username}'


@shared_task
def deactivate_inactive_accounts():
    """
    Deactivate accounts that have been inactive for more than a year.
    """
    one_year_ago = timezone.now() - timezone.timedelta(days=365)
    inactive_users = User.objects.filter(last_login__lt=one_year_ago, is_active=True)
    
    count = inactive_users.count()
    inactive_users.update(is_active=False)
    return f'Deactivated {count} inactive accounts'

@shared_task
def notify_user_of_new_device_login(user_id, device_info):
    """
    Notify user of a login from a new device.
    """
    user = User.objects.get(id=user_id)
    send_mail(
        subject='New Device Login Detected',
        message=f'Hello {user.username},\n\nWe detected a login to your account from a new device:\n\n{device_info}\n\nIf this was not you, please secure your account immediately.',
        from_email='noreply@theater.com',
        recipient_list=[user.email],
    )
    return f'Notified {user.username} of new device login'


@shared_task
def send_show_reminder():
    """
    Send reminder emails to users who have reservations for shows happening the next day.
    """
    tomorrow = timezone.now().date() + timezone.timedelta(days=1)
    reservations = Reservation.objects.filter(show__date=tomorrow, status='reserved')
    
    for reservation in reservations:
        send_mail(
            subject=f'Reminder: Your reservation for {reservation.show.title} is tomorrow!',
            message=f'Hello {reservation.user.username},\n\nThis is a reminder that you have a reservation for the show "{reservation.show.title}" at {reservation.show.time} on {reservation.show.date}.',
            from_email='noreply@theater.com',
            recipient_list=[reservation.user.email],
        )
    return f'Sent reminders for {reservations.count()} reservations'

@shared_task
def generate_daily_report():
    """
    Generate and email a daily report of reservations.
    """
    today = timezone.now().date()
    reservations = Reservation.objects.filter(show__date=today)
    
    report_content = f'Daily Report for {today}\n\nTotal Reservations: {reservations.count()}\n\n'
    for reservation in reservations:
        report_content += f'Reservation ID: {reservation.id}, User: {reservation.user.username}, Show: {reservation.show.title}, Seat: {reservation.seat.seat_number}, Status: {reservation.status}\n'
    
    send_mail(
        subject=f'Daily Report for {today}',
        message=report_content,
        from_email='noreply@theater.com',
        recipient_list=['admin@theater.com'],
    )
    return f'Sent daily report for {today}'

@shared_task
def send_payment_confirmation(reservation_id):
    """
    Send payment confirmation email to the user.
    """
    reservation = Reservation.objects.get(id=reservation_id)
    send_mail(
        subject='Payment Confirmation',
        message=f'Thank you {reservation.user.username} for your payment for the show "{reservation.show.title}" on {reservation.show.date} at {reservation.show.time}. Your seat number is {reservation.seat.seat_number}.',
        from_email='noreply@theater.com',
        recipient_list=[reservation.user.email],
    )
    return f'Sent payment confirmation for reservation {reservation_id}'

@shared_task
def notify_admin_of_new_reservation(reservation_id):
    """
    Notify admin of a new reservation.
    """
    reservation = Reservation.objects.get(id=reservation_id)
    send_mail(
        subject='New Reservation Notification',
        message=f'A new reservation has been made by {reservation.user.username} for the show "{reservation.show.title}" on {reservation.show.date} at {reservation.show.time}. Seat number: {reservation.seat.seat_number}.',
        from_email='noreply@theater.com',
        recipient_list=['admin@theater.com'],
    )
    return f'Notified admin of new reservation {reservation_id}'

