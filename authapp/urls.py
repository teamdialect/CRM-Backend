from django.urls import include, path
from authapp.views import SignUpViewSet, LoginViewSet, ProfileViewSet, LeadViewSet, TaskViewSet, HomeView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework import routers
app_name="authapp"

router = routers.DefaultRouter()
router.register(r'signup', SignUpViewSet, basename='signup')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'leads', LeadViewSet, basename='leads')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('homepage/',HomeView.as_view(), name='homepage'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]

urlpatterns += router.urls