from django.contrib.auth import authenticate

from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from rooms.models import Room
from rooms.serializer import RoomModelSerializer
from .models import User
from .serializers import UserSerializer


class UsersView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(data=UserSerializer(user).data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):
    """Profile API"""

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FavsView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        user = request.user
        serializer = RoomModelSerializer(user.favs.all(), many=True)
        return Response(data=serializer.data)

    def put(self, request):
        pk = request.data.get("pk", request.data.get("id", None))
        if pk is not None:
            try:
                room = Room.objects.get(pk=pk)
                user = request.user
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


@api_view(["GET"])
def user_detail(request, pk):
    if request.user.pk == pk:
        return Response(status=status.HTTP_403_FORBIDDEN)
    try:
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        user = authenticate(username=username, password=password)
    print(user)
    return Response(status=status.HTTP_200_OK)
