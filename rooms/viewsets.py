from rest_framework import viewsets
from .models import Room
from .serializer import DetailRoomSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = DetailRoomSerializer
