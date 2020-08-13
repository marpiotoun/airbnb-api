from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from .models import Room
from .serializer import RoomModelSerializer


class RoomsView(APIView):
    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        rooms = Room.objects.all()
        paginated_rooms = paginator.paginate_queryset(rooms, request)
        serialized_paginated_rooms = RoomModelSerializer(
            paginated_rooms, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serialized_paginated_rooms.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serialized_room = RoomModelSerializer(data=request.data)
        if serialized_room.is_valid():
            room = serialized_room.save(user=request.user)
            res = RoomModelSerializer(room).data
            return Response(data=res, status=status.HTTP_200_OK)
        else:
            return Response(
                data=serialized_room.errors, status=status.HTTP_400_BAD_REQUEST
            )


# @api_view(["GET", "POST"])
# def rooms_view(request):
#     if request.method == "GET":
#         rooms = Room.objects.all()[:5]
#         serialized_rooms = RoomSerializer(rooms, many=True)
#         return Response(serialized_rooms.data)
#     elif request.method == "POST":
#         if not request.user.is_authenticated:
#             return Response(status=status.HTTP_401_UNAUTHORIZED)
#         serialized_room = CreateRoomSerializer(data=request.data)
#         if serialized_room.is_valid():
#             room = serialized_room.save(user=request.user)
#             res = DetailRoomSerializer(room).data
#             return Response(data=res, status=status.HTTP_200_OK)
#         else:
#             return Response(
#                 data=serialized_room.errors, status=status.HTTP_400_BAD_REQUEST
#             )


# class ListRoomsView(ListAPIView):
#     serializer_class = RoomSerializer
#
#     def get_queryset(self):
#         return Room.objects.all()


# class ListRoomsView(APIView):
#     def get(self, request):
#         rooms = Room.objects.all()
#         serializer = RoomSerializer(rooms, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         pass


# @api_view(["get"])
# def list_rooms(request):
#     rooms = Room.objects.all()
#     serialized_rooms = RoomSerializer(rooms, many=True)
#     return Response(data=serialized_rooms.data)


class RoomView(APIView):
    @staticmethod
    def get_object(pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            return None

    def get(self, request, pk):
        room = self.get_object(pk)
        if room is not None:
            data = RoomModelSerializer(room, context={"request": request}).data
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        room = self.get_object(pk)
        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            serializer = RoomModelSerializer(room, data=request.data, partial=True)
            if serializer.is_valid():
                room = serializer.save()
                return Response(
                    data=RoomModelSerializer(room).data, status=status.HTTP_200_OK
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        room = self.get_object(pk)
        if room is not None:
            if request.user != room.user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            data = RoomModelSerializer(room).data
            room.delete()
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def room_search(request):
    max_price = request.GET.get("max_price", None)
    min_price = request.GET.get("min_price", None)
    beds = request.GET.get("beds", None)
    bedrooms = request.GET.get("bedrooms", None)
    bathrooms = request.GET.get("bathrooms", None)
    lat = request.GET.get("lat", None)
    lng = request.GET.get("lng", None)
    filter_kwargs = {}
    if max_price is not None:
        filter_kwargs["price__lte"] = max_price
    if min_price is not None:
        filter_kwargs["price__gte"] = min_price
    if beds is not None:
        filter_kwargs["beds"] = beds
    if bedrooms is not None:
        filter_kwargs["bedrooms"] = bedrooms
    if bathrooms is not None:
        filter_kwargs["bathrooms"] = bathrooms
    if lat is not None and lng is not None:
        filter_kwargs["lat__lte"] = float(lat) + 0.005
        filter_kwargs["lat__gte"] = float(lat) - 0.005
        filter_kwargs["lng__lte"] = float(lng) + 0.005
        filter_kwargs["lng__gte"] = float(lng) - 0.005
    try:
        rooms = Room.objects.filter(**filter_kwargs)
    except ValueError:
        rooms = Room.objects.all()

    paginator = PageNumberPagination()
    paginator.page_size = 10

    results = paginator.paginate_queryset(rooms, request)
    serializer = RoomModelSerializer(results, many=True)
    return paginator.get_paginated_response(serializer.data)
