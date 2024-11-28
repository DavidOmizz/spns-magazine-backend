from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import ArticleViewSet, EditionViewSet, ContributorViewSet, RegisterView, LoginView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'editions', EditionViewSet)
router.register(r'contributors', ContributorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # For login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # For refreshing token
]