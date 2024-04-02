from django.urls import include, path
from authapp.views import DeleteViewSet, SignUpViewSet, LoginViewSet, UpdateViewSet, LeadViewSet, TaskViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'signup', SignUpViewSet, basename='signup')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'update', UpdateViewSet, basename='update')
router.register(r'delete', DeleteViewSet, basename='delete')
router.register(r'leads', LeadViewSet, basename='leads')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]