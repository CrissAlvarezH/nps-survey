from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from nps.models import Company, CompanyUser
from nps.serializers.companies import (
    CompanyCreateSerializer,
    CompanyListSerializer,
    CompanyRetrieveSerializer,
    CompanyUserCreateSerializer,
    CompanyUserListSerializer,
    CompanyUserUpdateSerializer
)
from nps.services.companies import (
    add_person_to_company,
    company_exist_by_id,
    person_company_relationship_exists,
    remove_person_from_company,
    update_person_rol
)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all().order_by("id")
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return CompanyListSerializer
        elif self.action == "retrieve":
            return CompanyRetrieveSerializer
        elif self.action in ["create", "update"]:
            return CompanyCreateSerializer


class CompanyUserRelationshipViewSet(viewsets.ModelViewSet):
    serializer_class = CompanyUserListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CompanyUser.objects.filter(
            company__id=self.kwargs["company_id"]
        ).order_by("id")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["company_id"] = self.kwargs["company_id"]
        return context

    def create(self, request, company_id):
        if not company_exist_by_id(id=company_id):
            raise ValidationError("Company does not exists")

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

        output_data = CompanyUserListSerializer(relationship).data
        return Response(output_data, status=status.HTTP_201_CREATED)

    def update(self, request, pk, company_id):
        if not company_exist_by_id(id=company_id):
            raise ValidationError("Company does not exists")

        if not person_company_relationship_exists(
            user_id=pk, company_id=company_id
        ):
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CompanyUserUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        relationship = update_person_rol(
            user_id=pk, company_id=company_id, role=data["role"]
        )

        output_data = CompanyUserListSerializer(relationship).data
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
