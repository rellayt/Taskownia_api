from rest_framework import serializers
from .models import User, Address, PersonalData
from django.contrib.auth.hashers import make_password

from .utils import hashPassword


class PersonalDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PersonalData
        fields = ['first_name', 'last_name', 'phone', 'birth_date']


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ['city', 'state', 'country', 'country_code']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    address = AddressSerializer
    persona_data = PersonalDataSerializer

    class Meta:
        model = User
        fields = ['name', 'email', 'address', 'personal_data']

    # def create(self, validated_data):
    #     password = validated_data.pop('password', None)
    #     instance = self.Meta.model(**validated_data)
    #     hashedPassword = hashPassword(password)
    #     if password is not None:
    #         instance.set_password(hashedPassword)
    #     instance.save()
    #     return instance

