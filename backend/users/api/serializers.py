from rest_framework import serializers

from backend.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["username", "password", "email", "is_staff", "name"]
        extra_kwargs = {
            # "url": {"view_name": "api:user-detail", "lookup_field": "username"},
            # 'id': {'read_only': True},
            'password': {'write_only': True}
        }
    
    def create(self,validated_data):
        user = User(username = validated_data['username'],email=validated_data["email"])
        user.set_password(validated_data['password'])
        user.save()
    
        return user

