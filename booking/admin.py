from django.contrib import admin
from .models import Theater, Show, Seat, Reservation, Ticket
from .forms import TheaterCreationForm

class SeatInline(admin.TabularInline):
    model = Seat
    extra = 0
    readonly_fields = ('seat_number', 'is_reserved')

class ReservationInline(admin.TabularInline):
    model = Reservation
    extra = 0
    readonly_fields = ('user', 'seat', 'id', 'reserved_at')

class ShowAdmin(admin.ModelAdmin):
    list_display = ('theater', 'title', 'description', 'date', 'time')
    search_fields = ('theater__name', 'title', 'date')
    list_filter = ('theater__name', 'date', 'time')
    inlines = [ ReservationInline]

class TheaterAdmin(admin.ModelAdmin):
    form = TheaterCreationForm
    list_display = ('name', 'location', 'total_seats')
    search_fields = ('name', 'location')
    list_filter = ('location',)

    def total_seats(self, obj):
        return obj.seat_set.count()
    total_seats.short_description = 'Total Seats'

    def save_model(self, request, obj, form, change):
        obj.save()
        num_seats = form.cleaned_data['num_seats']
        if not change:  # Only create seats if it's a new object
            seats = [Seat(theater=obj, seat_number=i) for i in range(1, num_seats + 1)]
            Seat.objects.bulk_create(seats)

class SeatAdmin(admin.ModelAdmin):
    list_display = ('theater', 'seat_number', 'is_reserved')
    search_fields = ('theater', 'seat_number')
    list_filter = ('theater', 'is_reserved')

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'show', 'seat', 'id', 'reserved_at')
    search_fields = ('user__username', 'show__title', 'id')
    list_filter = ('show__title', 'user__username', 'reserved_at')

class TicketAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'ticket_number', 'issued_at')
    search_fields = ('reservation__id', 'ticket_number')
    list_filter = ('reservation__show__title', 'issued_at')

admin.site.register(Theater, TheaterAdmin)
admin.site.register(Show, ShowAdmin)
admin.site.register(Seat, SeatAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Ticket, TicketAdmin)
