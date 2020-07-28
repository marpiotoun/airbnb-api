from django.urls import path
from . import views
from . import viewsets
from rest_framework.routers import DefaultRouter

app_name = "rooms"

router = DefaultRouter()
router.register(r"", viewsets.RoomViewSet, basename="room")
urlpatterns = router.urls


#
# urlpatterns += [
#     path("list/", views.RoomsView.as_view()),
#     path("<int:pk>/", views.RoomView.as_view()),
#     path("search/", views.room_search),
# ]
