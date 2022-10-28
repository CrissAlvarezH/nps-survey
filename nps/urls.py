from email.mime import base
from rest_framework.routers import DefaultRouter

from nps.views.companies import CompanyUserRelationshipViewSet, CompanyViewSet
from nps.views.nps import NpsReportsViewSet, NpsViewSet


router = DefaultRouter()

router.register("companies", CompanyViewSet, basename="companies")
router.register(
    r"companies/(?P<company_id>\d+)/persons",
    CompanyUserRelationshipViewSet,
    basename="company-persons"
)
router.register("surveys", NpsViewSet, basename="surveys")
router.register("reports", NpsReportsViewSet, basename="reports")

urlpatterns = router.urls
