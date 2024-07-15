from django import forms
from .models import Theater, Seat

class TheaterCreationForm(forms.ModelForm):
    num_seats = forms.IntegerField(label="Number of Seats", min_value=1)

    class Meta:
        model = Theater
        fields = ['name', 'location', 'num_seats']

    def save(self, commit=True):
        theater = super().save(commit=False)
        num_seats = self.cleaned_data['num_seats']
        
        if commit:
            theater.save()
            seats = [Seat(theater=theater, seat_number=i) for i in range(1, num_seats + 1)]
            Seat.objects.bulk_create(seats)
        return theater
