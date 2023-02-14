from rest_framework import serializers
from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=4, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password',]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
