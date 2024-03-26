from django.urls import include, path
from authapp.views import DeleteViewSet, SignUpViewSet, LoginViewSet, UpdateViewSet, LeadViewSet

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'signup', SignUpViewSet, basename='signup')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'update', UpdateViewSet, basename='update')
router.register(r'delete', DeleteViewSet, basename='delete')
router.register(r'leads', LeadViewSet, basename='leads')


urlpatterns = [
    path('', include(router.urls)),
]