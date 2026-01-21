from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.views import ObtainAuthToken

from backend.users.models import User

from .serializers import UserSerializer


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    
    
class UserRegisterationView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def post(self,request, *args, **kwargs):
        serializer = self.serializer_class(data =request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message":"Registration successfull!"},status=status.HTTP_201_CREATED)
        return Response({"message":"Registration Failed!"},status=status.HTTP_400_BAD_REQUEST)
 
        
class UserLoginTokenView(ObtainAuthToken):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email if user.email else None ,
            'is_staff': user.is_staff
        }, status=status.HTTP_200_OK)

