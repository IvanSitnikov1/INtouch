from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import *

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('assignments', AssignmentViewSet, basename='assignments')
router.register('massage', MassageViewSet, basename='massage')

urlpatterns = [
    path('', include(router.urls)),
    path('drf-auth/', include('rest_framework.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', EmailLoginView.as_view(), name='login'),
    path('clients/', ClientListView.as_view(), name='clients'),
    path('clients/add/', AddClientView.as_view(), name='add_client'),
    path(
        'confirm-email/<int:pk>/<str:token>/',
        UserConfirmEmailView.as_view(),
        name='confirm_email'
    ),
    path(
        'password/reset/',
        PasswordResetRequestView.as_view(),
        name='password_reset'
    ),
    path(
        'password/reset/confirm/<int:pk>/<str:token>/',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'password/reset/complete/',
        PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    )
]
