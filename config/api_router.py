from django.urls import path
from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter
from backend.users.api.views import UserViewSet, UserRegisterationView, UserLoginTokenView


router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"

urlpatterns = [
    path("v1/register/", UserRegisterationView.as_view(), name="register"),
    path("v1/login/", UserLoginTokenView.as_view(), name="login"),

]

urlpatterns += router.urls

