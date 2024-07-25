from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Theater, Show, Seat, Reservation
from .serializers import (
    TheaterSerializer, ShowSerializer, SeatSerializer,
    ReservationSerializer
)

class HomeView(View):
    def get(self, request):
        return render(request, 'booking/home.html')

class SignupView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return render(request, 'registration/signup.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return render(request, 'registration/login.html', {'form': form})

@login_required
def LogoutView(request):
    logout(request)
    return redirect('home')

class SearchTheatersView(View):
    def get(self, request):
        location = request.GET.get('location')
        if location:
            theaters = Theater.objects.filter(location=location)
            return render(request, 'booking/search_theaters.html', {'theaters': theaters})
        return render(request, 'booking/search_theaters.html')

@login_required
def block_seats(request, show_id):
    if request.method == 'POST':
        show = Show.objects.get(id=show_id)
        seat_number = request.POST.get('seat_number')
        reservation_id = f"reserve_{show_id}_{request.user.id}"
        Reservation.objects.create(user=request.user, show=show, seat_number=seat_number, reservation_id=reservation_id)
        return redirect('book_tickets', reservation_id=reservation_id)
    return render(request, 'booking/block_seats.html', {'show_id': show_id})

@login_required
def book_tickets(request, reservation_id):
    if request.method == 'POST':
        reservation = Reservation.objects.get(reservation_id=reservation_id, user=request.user)
        ticket_id = f"ticket_{reservation.id}"
        reservation.ticket_id = ticket_id
        reservation.save()
        return render(request, 'booking/book_tickets.html', {'ticket_id': ticket_id})
    return render(request, 'booking/book_tickets.html', {'reservation_id': reservation_id})

# API views

class TheaterCreateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = TheaterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TheaterListAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        location = request.query_params.get('location')
        if location:
            theaters = Theater.objects.filter(location=location)
        else:
            theaters = Theater.objects.all()

        if not theaters:
            return Response({'message': 'No theaters found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TheaterSerializer(theaters, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ShowListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        theater_id = request.query_params.get('theater_id')
        if theater_id:
            shows = Show.objects.filter(theater_id=theater_id)
        else:
            shows = Show.objects.all()
        serializer = ShowSerializer(shows, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ShowCreateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = ShowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SeatListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        show_id = request.query_params.get('show_id')
        if show_id:
            seats = Seat.objects.filter(show_id=show_id)
        else:
            seats = Seat.objects.all()
        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SeatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReservationListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        reservations = Reservation.objects.filter(user=request.user)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ReservationCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookTicketsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        reservation_id = request.data.get('reservation_id')
        reservation = Reservation.objects.get(reservation_id=reservation_id, user=request.user)
        ticket_id = f"ticket_{reservation.id}"
        reservation.ticket_id = ticket_id
        reservation.save()
        return Response({'ticket_id': ticket_id}, status=status.HTTP_200_OK)
