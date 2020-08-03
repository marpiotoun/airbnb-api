import jwt

from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from django.conf import settings
from django.contrib.auth import authenticate

from rooms.models import Room
from rooms.serializer import RoomModelSerializer
from .permissions import IsSelf
from .serializers import UserSerializer
from .models import User


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == "list":
            permission_classes = [permissions.IsAdminUser]
        elif self.action in ["create", "retrieve", "favs"]:
            permission_classes = [permissions.AllowAny]
        else:
            # action in [destroy, update, partial_update]
            permission_classes = [
                IsSelf,
            ]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["post"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            user = authenticate(username=username, password=password)
        if user is not None:
            encoded = jwt.encode(
                {"id": user.pk}, settings.SECRET_KEY, algorithm="HS256"
            )
            return Response(data={"token": encoded, "id": user.pk})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True)
    def favs(self, request, pk):
        user = self.get_object()
        serializer = RoomModelSerializer(user.favs.all(), many=True)
        return Response(data=serializer.data)

    @favs.mapping.put
    def toggle_favs(self, request, pk):
        pk = request.data.get("pk", request.data.get("id", None))
        if pk is not None:
            try:
                room = Room.objects.get(pk=pk)
                user = self.get_object()
                if room in user.favs.all():
                    user.favs.remove(room)
                else:
                    user.favs.add(room)
                user.save()
                serializer = RoomModelSerializer(user.favs.all(), many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            except Room.DoesNotExist:
                pass
        return Response(status=status.HTTP_400_BAD_REQUEST)
