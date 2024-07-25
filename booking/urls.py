from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HomeView, SignupView, LoginView, LogoutView,
    TheaterCreateAPIView, TheaterListAPIView, ShowListAPIView,ShowCreateAPIView, SeatListCreateAPIView,
    ReservationCreateAPIView, BookTicketsAPIView, ReservationListAPIView
)

# Router for ViewSets
router = DefaultRouter()

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView, name='logout'),
    
    # API endpoints
    path('api/', include(router.urls)),
    path('api/theaters/add', TheaterCreateAPIView.as_view(), name='theater-create'),
    path('api/theaters/', TheaterListAPIView.as_view(), name='theater-list'),
    path('api/shows/add', ShowCreateAPIView.as_view(), name='show-create'),
    path('api/shows/', ShowListAPIView.as_view(), name='show-list'),
    path('api/seats/', SeatListCreateAPIView.as_view(), name='seat-list-create'),
    path('api/reservations/', ReservationListAPIView.as_view(), name='reservation-list'),
    path('api/reservations/add', ReservationCreateAPIView.as_view(), name='reservation-create'),
    path('api/tickets/', BookTicketsAPIView.as_view(), name='ticket-list-create'),
]
