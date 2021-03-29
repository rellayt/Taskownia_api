from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

from .utils import hashPassword

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
    # def create(self, validated_data):
    #     password = validated_data.pop('password', None)
    #     instance = self.Meta.model(**validated_data)
    #     hashedPassword = hashPassword(password)
    #     if password is not None:
    #         instance.set_password(hashedPassword)
    #     instance.save()
    #     return instance
