from dataclasses import fields
from distutils.command.upload import upload
from pkg_resources import require
from rest_framework import serializers

from .utils import upload_file
from .models import User, Record
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    name = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'name', 'is_active']
        
    


class VerifySerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ['email', 'is_active', 'name']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
                        required=True,
                        validators=[UniqueValidator(queryset=User.objects.all())]
                    )
    name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required= True)

    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Password fields didn\'t match.'})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['email'],
            email = validated_data['email'],
            name = validated_data['name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class RecordSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)
    file = serializers.FileField(
        write_only=True,
        max_length=None,
        allow_empty_file=False,
        use_url=True
    )
    uri = serializers.CharField(read_only=True)

    class Meta:
        model = Record
        fields = ['id','name', 'file', 'uri']

    def create(self, validated_data):

        request = self.context.get('request')

        file = request.FILES.get('file')

        uri = upload_file(file)

        record = Record.objects.create(
            user = request.user,
            name = validated_data['name'],
            uri = uri
        )
        
        record.save()

        return record