from rest_framework import serializers
from .models import User, Address, PersonalData, Project
from django.contrib.auth.hashers import make_password

from .utils import hashPassword


class PersonalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalData
        fields = ['first_name', 'last_name', 'phone', 'birth_date']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['city', 'state', 'country', 'zip_code']


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=False)
    personal_data = PersonalDataSerializer(many=False)

    class Meta:
        model = User
        fields = ['name', 'email', 'address', 'personal_data']


class ProjectSerializer(serializers.ModelSerializer):
    maker = UserSerializer(many=False)
    author = UserSerializer(many=False)

    class Meta:
        model = Project
        fields = ['id', 'title', 'desc', 'created_at', 'author', 'maker']

    # def create(self, validated_data):
    #     password = validated_data.pop('password', None)
    #     instance = self.Meta.model(**validated_data)
    #     hashedPassword = hashPassword(password)
    #     if password is not None:
    #         instance.set_password(hashedPassword)
    #     instance.save()
    #     return instance
