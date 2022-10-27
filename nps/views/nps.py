from rest_framework import viewsets, status, mixins
from rest_framework.response import Response

from nps.serializers.nps import NpsCreateSerializer, NpsRetrieveSerializer
from nps.services.nps import nps_create, nps_list


class NpsViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = nps_list()
    serializer_class = NpsRetrieveSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return nps_list(answer__gt=4)
        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        user = request.user if not request.user.is_anonymous else None

        serializer = NpsCreateSerializer(
            data=request.data,
            context={"user_id": user.id if user else None}
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        nps = nps_create(
            user=user,
            company_id=data["company_id"],
            answer=data["answer"]
        )

        output_data = NpsRetrieveSerializer(nps).data
        return Response(output_data, status=status.HTTP_201_CREATED)


class NpsReportsViewSet(viewsets.ViewSet):
    pass
