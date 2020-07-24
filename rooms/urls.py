from django.urls import path
from . import views
from . import viewsets
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r"", viewsets.RoomViewSet, basename="room")
# urlpatterns = router.urls


app_name = "rooms"

urlpatterns = [
    path("list/", views.RoomsView.as_view()),
    path("<int:pk>/", views.RoomView.as_view()),
]
