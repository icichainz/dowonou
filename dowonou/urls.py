"""
URL configuration for dowonou project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from main.api import (
    UserViewSet, CategoryViewSet, ToolViewSet, RentalViewSet,
    ReviewViewSet, TransactionViewSet, NotificationViewSet,
    UserVerificationViewSet, InsuranceViewSet, DisputeViewSet,
    MaintenanceViewSet, PromotionalCampaignViewSet, UserPreferencesViewSet
)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'tools', ToolViewSet)
router.register(r'rentals', RentalViewSet, basename='rental')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'transactions', TransactionViewSet)
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'verifications', UserVerificationViewSet, basename='verification')
router.register(r'insurance', InsuranceViewSet, basename='insurance')
router.register(r'disputes', DisputeViewSet, basename='dispute')
router.register(r'maintenance', MaintenanceViewSet, basename='maintenance')
router.register(r'campaigns', PromotionalCampaignViewSet)
router.register(r'preferences', UserPreferencesViewSet, basename='preferences')

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('main.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
