from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if not user:
            raise serializers.ValidationError("Username or password is invalid.")
        data['user'] = user
        return data

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']

    def validate_email(self, email):
        if not email or "@" not in email:
            raise serializers.ValidationError("Invalid email.")
        return email

    def validate(self, data):
        if User.objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError("Username already taken.")
        if data.get("email") and User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError("Email already used.")
        return data
