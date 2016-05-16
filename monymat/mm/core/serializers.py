__author__ = 'rajaprasanna'

from rest_framework import serializers
from . import models

class SignupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    full_name = serializers.ReadOnlyField(source='get_full_name')
    auth_token = serializers.ReadOnlyField(source='get_auth_token')
    # todo validation still pending

    class Meta:
        model = models.User
        fields = ('name', 'email', 'password', 'mobile', 'address', 'full_name', 'auth_token')

    def validate_mobile(self, mobile):
        # print(self.initial_data)
        if not mobile:
            raise serializers.ValidationError("email is required")
        if models.User.objects.filter(mobile=mobile).exists():
            raise serializers.ValidationError("This email id is already registered with us. Please login")
        return mobile

    def create(self, validated_data):
        # validated_data['username'] = validated_data['email']
        name = validated_data.pop('name')
        first_name, last_name = name.split(' ')[0], " ".join(name.split(' ')[1:])
        validated_data['first_name'] = first_name.capitalize()
        validated_data['last_name'] = last_name
        user = models.User.objects.create_user(validated_data.get('mobile'), **validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=True)
    password = serializers.CharField(max_length=32, required=True)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('mobile', 'address', 'first_name', 'last_name')

