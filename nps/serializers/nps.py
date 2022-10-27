from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from nps.models import Nps
from nps.serializers.companies import CompanyUserRetrieveSerializer
from nps.services.companies import (
    company_exist_by_id,
    person_company_relationship_exists
)


class NpsRetrieveSerializer(serializers.ModelSerializer):
    person = CompanyUserRetrieveSerializer(allow_null=True)

    class Meta:
        model = Nps
        fields = "__all__"


class NpsCreateSerializer(serializers.Serializer):
    company_id = serializers.IntegerField()
    answer = serializers.IntegerField()

    def validate_company_id(self, value):
        if not company_exist_by_id(id=value):
            raise ValidationError("this company does not exists")

        user_id = self.context.get("user_id")
        if user_id:
            if not person_company_relationship_exists(
                user_id=user_id, company_id=value
            ):
                raise ValidationError("This user is not in this company")

        return value

    def validate_answer(self, value):
        if value > 10 and value < 1:
            raise ValidationError("answer invalid, valid values: 1 - 10")

        return value
