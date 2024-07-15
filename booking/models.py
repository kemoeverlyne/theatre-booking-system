from django.db import models
from django.contrib.auth.models import User

class Theater(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    total_seats = models.IntegerField(default=0)

    def __str__(self):
        return f"Theater: {self.name} - Location: {self.location}"

    class Meta:
        ordering = ['name']

class Show(models.Model):
    theater = models.ForeignKey(Theater, related_name='shows', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()

    class Meta:
        unique_together = ('theater', 'date', 'time')
        ordering = ['date', 'time']

    def __str__(self):
        return f"Show: {self.title} at {self.theater.name} on {self.date} at {self.time}"

class Seat(models.Model):
    theater = models.ForeignKey(Theater, related_name='seats', on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    is_reserved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('theater', 'seat_number')
        ordering = ['seat_number']

    def __str__(self):
        return f"Seat {self.seat_number} in {self.theater.name}"

class SeatPricing(models.Model):
    seat = models.ForeignKey(Seat, related_name='pricing', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pricing for Seat {self.seat.seat_number} in {self.seat.theater.name}: {self.price}"

    class Meta:
        ordering = ['seat__seat_number']

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('reserved', 'Reserved'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, related_name='reservations', on_delete=models.CASCADE)
    show = models.ForeignKey(Show, related_name='reservations', on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, related_name='reservations', on_delete=models.CASCADE)
    reserved_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='reserved')

    class Meta:
        unique_together = ('show', 'seat')
        ordering = ['reserved_at']

    def __str__(self):
        return f"Reservation by {self.user.username} for {self.show.title} on {self.show.date} at {self.show.time} - Status: {self.status}"

class Ticket(models.Model):
    reservation = models.OneToOneField(Reservation, related_name='ticket', on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=50, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['issued_at']

    def __str__(self):
        return f"Ticket {self.ticket_number} for Reservation {self.reservation}"