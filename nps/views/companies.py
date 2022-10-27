from rest_framework import viewsets, status
from rest_framework.response import Response

from nps.models import Company, CompanyUser
from nps.serializers.companies import (
    CompanyListSerializer,
    CompanyRetrieveSerializer,
    CompanyUserCreateSerializer,
    CompanyUserRetrieveSerializer,
    CompanyUserUpdateSerializer
)
from nps.services.companies import (
    add_person_to_company,
    person_company_relationship_exists,
    remove_person_from_company,
    update_person_rol
)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CompanyListSerializer
        elif self.action == "retrieve":
            return CompanyRetrieveSerializer


class CompanyUserRelationshipViewSet(viewsets.ModelViewSet):
    serializer_class = CompanyUserRetrieveSerializer

    def get_queryset(self):
        return CompanyUser.objects.filter(
            company__id=self.kwargs["company_id"]
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["company_id"] = self.kwargs["company_id"]
        return context

    def create(self, request, company_id):
        serializer = CompanyUserCreateSerializer(
            data=request.data,
            context={"company_id": company_id}
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        relationship = add_person_to_company(
            user_id=data["user"]["id"],
            company_id=company_id,
            role=data["role"]
        )

        output_data = CompanyUserRetrieveSerializer(relationship).data
        return Response(output_data, status=status.HTTP_201_CREATED)

    def update(self, request, pk, company_id):
        serializer = CompanyUserUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        relationship = update_person_rol(
            user_id=pk, company_id=company_id, role=data["role"]
        )

        output_data = CompanyUserRetrieveSerializer(relationship).data
        return Response(output_data)

    def destroy(self, request, pk, company_id):
        if not person_company_relationship_exists(
            user_id=pk, company_id=company_id
        ):
            return Response(status=status.HTTP_404_NOT_FOUND)

        remove_person_from_company(
            company_id=company_id, user_id=pk
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
