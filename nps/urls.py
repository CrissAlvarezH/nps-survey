from rest_framework.routers import DefaultRouter

from nps.views.companies import CompanyUserRelationshipViewSet, CompanyViewSet


router = DefaultRouter()

router.register("companies", CompanyViewSet, basename="companies")
router.register(
    r"companies/(?P<company_id>\d+)/persons",
    CompanyUserRelationshipViewSet,
    basename="company-persons"
)

urlpatterns = router.urls
