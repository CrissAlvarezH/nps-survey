# Rest framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from nps.models import Company

from users.services import user_create
# Local
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'full_name', 'email')


class UserRetrieveSerializer(serializers.ModelSerializer):
    class UserCompany(serializers.ModelSerializer):
        class Meta:
            model = Company
            fields = ("id", "name", "country_name", "total_persons")

    companies = UserCompany(many=True)

    class Meta:
        model = User
        fields = ("id", "full_name", "email", "companies")


class UserSignUpSerializer(serializers.Serializer):
    full_name = serializers.CharField(min_length=1, max_length=500)
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    password = serializers.CharField(min_length=5, max_length=20)
    password_confirmation = serializers.CharField(min_length=5, max_length=20)

    def validate(self, data):
        # Validate if password and password_confirmation is the same
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError('Passwords are not equals')

        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        return user_create(**validated_data)
