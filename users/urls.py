from django.urls import path
from .viewsets import UserViewSet
from rest_framework import routers

app_name = "users"
router = routers.DefaultRouter()
router.register(r"", UserViewSet, basename="user")
urlpatterns = router.urls

#
# urlpatterns = [
#     path("", views.UsersView.as_view()),
#     path("login/", views.login),
#     path("me/", views.MeView.as_view()),
#     path("me/fav/", views.FavsView.as_view()),
#     path("<int:pk>/", views.user_detail),
# ]
