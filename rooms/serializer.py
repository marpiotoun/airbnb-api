from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Room
        fields = ("pk", "name", "price", "user")


class DetailRoomSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Room
        exclude = ("modified",)


class RoomModelSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_fav = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            "id",
            "user",
            "created",
            "name",
            "address",
            "price",
            "beds",
            "lat",
            "lng",
            "bedrooms",
            "bathrooms",
            "check_in",
            "check_out",
            "instant_book",
            "is_fav",
        )
        read_only_fields = (
            "id",
            "user",
            "created",
        )

    def get_is_fav(self, obj):
        request = self.context.get("request", None)
        if request is not None:
            user = request.user
            if user.is_authenticated:
                return obj in user.favs.all()
        return False

    def validate(self, data):
        if not self.instance:
            # Create instance
            check_in = data.get("check_in")
            check_out = data.get("check_out")
            if check_in == check_out:
                raise serializers.ValidationError(
                    "Check in and Check out must not be same time"
                )
            else:
                return data
        else:
            # Updating instance
            check_in = data.get("check_in", self.instance.check_in)
            check_out = data.get("check_out", self.instance.check_out)
            if check_in == check_out:
                raise serializers.ValidationError(
                    "Check in and Check out must not be same time"
                )
            else:
                return data

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        room = Room.objects.create(**validated_data, user=user)
        return room


#
# class CreateRoomSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=140)
#     address = serializers.CharField(max_length=140)
#     price = serializers.IntegerField(help_text="USD per night")
#     beds = serializers.IntegerField(default=1)
#     lat = serializers.DecimalField(max_digits=10, decimal_places=6)
#     lng = serializers.DecimalField(max_digits=10, decimal_places=6)
#     bedrooms = serializers.IntegerField(default=1)
#     bathrooms = serializers.IntegerField(default=1)
#     check_in = serializers.TimeField(default="00:00:00")
#     check_out = serializers.TimeField(default="00:00:00")
#     instant_book = serializers.BooleanField(default=False)
#
#     def create(self, validated_data):
#         return Room.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get("name", instance.name)
#         instance.address = validated_data.get("address", instance.address)
#         instance.price = validated_data.get("price", instance.price)
#         instance.beds = validated_data.get("beds", instance.beds)
#         instance.lat = validated_data.get("lat", instance.lat)
#         instance.lng = validated_data.get("lng", instance.lng)
#         instance.bedrooms = validated_data.get("bedrooms", instance.bedrooms)
#         instance.bathrooms = validated_data.get("bathrooms", instance.bathrooms)
#         instance.check_in = validated_data.get("check_in", instance.check_in)
#         instance.check_out = validated_data.get("check_out", instance.check_out)
#         instance.instant_book = validated_data.get(
#             "instant_book", instance.instant_book
#         )
#         instance.save()
#         return instance
#
#     def validate(self, data):
#         if not self.instance:
#             # Create instance
#             check_in = data.get("check_in")
#             check_out = data.get("check_out")
#             if check_in == check_out:
#                 raise serializers.ValidationError(
#                     "Check in and Check out must not be same time"
#                 )
#             else:
#                 return data
#         else:
#             # Updating instance
#             check_in = data.get("check_in", self.instance.check_in)
#             check_out = data.get("check_out", self.instance.check_out)
#             print(check_in, check_out)
#             if check_in == check_out:
#                 raise serializers.ValidationError(
#                     "Check in and Check out must not be same time"
#                 )
#             else:
#                 return data
