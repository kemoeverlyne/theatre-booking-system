from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HomeView, SignupView, LoginView, LogoutView,
    TheaterListCreateAPIView, ShowListCreateAPIView, SeatListCreateAPIView,
    ReservationCreateAPIView, BookTicketsAPIView
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
    path('api/theaters/', TheaterListCreateAPIView.as_view(), name='theater-list-create'),
    path('api/shows/', ShowListCreateAPIView.as_view(), name='show-list-create'),
    path('api/seats/', SeatListCreateAPIView.as_view(), name='seat-list-create'),
    path('api/reservations/', ReservationCreateAPIView.as_view(), name='reservation-list-create'),
    path('api/tickets/', BookTicketsAPIView.as_view(), name='ticket-list-create'),
]
