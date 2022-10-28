from typing import Callable, Tuple
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from nps.models import CompanyUser
from nps.serializers.companies import CompanyUserListSerializer, CompanyUserRetrieveSerializer

from nps.serializers.nps import NpsCreateSerializer, NpsRetrieveSerializer
from nps.services.countries import country_list
from nps.services.nps import get_detractors_top_by_country, get_edge_top_by_country, get_promoters_top_by_country, nps_create, nps_list
from nps import signals


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
            answer=data["answer"],
        )

        signals.nps_inserted.send(
            sender=self.__class__,
            nps_id=nps.id,
            request=self.request
        )

        output_data = NpsRetrieveSerializer(nps).data
        return Response(output_data, status=status.HTTP_201_CREATED)


class NpsReportsViewSet(viewsets.ViewSet):

    def serialize_top(self, filter_function: Callable, is_edge_top: bool = False) -> dict:
        def serialize(data, **kwargs):
            if data is None:
                return None
            return CompanyUserRetrieveSerializer(data, **kwargs).data

        data = {}
        for country in country_list():
            top = filter_function(country=country.name)
            if is_edge_top:
                top = {
                    "best_promoter": serialize(top[0]),
                    "worse_detractor": serialize(top[1])
                }
            else:
                top = serialize(top, many=True)
            if top:
                data[country.name] = top
        return data

    @action(detail=False, methods=["GET"], url_path="detractors-top")    
    def detractors_top(self, request):
        data = self.serialize_top(get_detractors_top_by_country)
        return Response(data)

    @action(detail=False, methods=["GET"], url_path="promoters-top")
    def promoters_top(self, request):
        data = self.serialize_top(get_promoters_top_by_country)
        return Response(data)

    @action(detail=False, methods=["GET"], url_path="edge-top")
    def edge_top(self, request):
        data = self.serialize_top(get_edge_top_by_country, is_edge_top=True)
        return Response(data)
