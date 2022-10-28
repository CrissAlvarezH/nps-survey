from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from nps.models import Company, CompanyUser
from nps.services.companies import person_company_relationship_exists

from users.serializers import UserSerializer
from users.services import user_exists_by_id


class CompanyUserCreateSerializer(serializers.Serializer):
    class UserRelationship(serializers.Serializer):
        id = serializers.IntegerField()

    user = UserRelationship()
    role = serializers.ChoiceField(choices=CompanyUser.Roles.choices)

    def validate(self, attrs):
        if not user_exists_by_id(id=attrs["user"]["id"]):
            raise ValidationError("This persons does not exists")

        if person_company_relationship_exists(
            user_id=attrs["user"]["id"], company_id=self.context["company_id"]
        ):
            raise ValidationError("This persons is already on this company")

        return super().validate(attrs)


class CompanyUserUpdateSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=CompanyUser.Roles.choices)



class CompanyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class CompanyListSerializer(serializers.ModelSerializer):
    total_persons = serializers.IntegerField()

    class Meta:
        model = Company
        fields = ["id", "name", "description", "country_name", "total_persons"]


class CompanyUserListSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = CompanyUser
        fields = ["user", "role"]


class CompanyRetrieveSerializer(serializers.ModelSerializer):
    persons = CompanyUserListSerializer(source="companyuser_set", many=True)

    class Meta:
        model = Company
        fields = ["id", "name", "description", "country_name", "persons"]


class CompanyUserRetrieveSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    company = CompanyListSerializer()

    class Meta:
        model = CompanyUser
        fields = ["user", "company", "role"]
