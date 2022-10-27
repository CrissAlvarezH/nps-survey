from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from nps.models import Nps


class NpsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nps
        fields = "__all__"


class NpsCreateSerializer(serializers.Serializer):
    answer = serializers.IntegerField()

    def validate_answer(self, value):
        if value > 10 and value < 1:
            raise ValidationError("answer invalid, valid values: 1 - 10")

        return value
