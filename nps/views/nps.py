from rest_framework import viewsets, status, mixins
from rest_framework.response import Response

from nps.serializers.nps import NpsCreateSerializer, NpsSerializer
from nps.models import Nps
from nps.services.nps import nps_create


class NpsViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Nps.objects.all()
    serializer_class = NpsSerializer

    def create(self, request, *args, **kwargs):
        serializer = NpsCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        user = request.user if not request.user.is_anonymous else None
        nps = nps_create(user=user, answer=data["answer"])

        output_data = NpsSerializer(nps).data
        return Response(output_data, status=status.HTTP_201_CREATED)
