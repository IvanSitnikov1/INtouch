from rest_framework import serializers

from main.models import *


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'accept_policy')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        if attrs['accept_policy'] == False:
            raise serializers.ValidationError("Accept with company policy")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['first_name'] + ' ' + validated_data['last_name'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
            accept_policy=validated_data['accept_policy'],
        )
        return user


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'


class MassageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Massage
        fields = '__all__'