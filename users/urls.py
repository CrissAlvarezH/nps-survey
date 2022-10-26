# Django
from django.urls import path, include
# Rest framework
from rest_framework.routers import DefaultRouter
# JWT
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# Local
from .views import UserViewSet


auth_urls = [
    path('', TokenObtainPairView.as_view(), name='auth'),
    path('refresh/', TokenRefreshView.as_view(), name='auth_refresh'),
]

router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')


urlpatterns = [
    path('auth/', include(auth_urls)),
    path('', include(router.urls)),
]

