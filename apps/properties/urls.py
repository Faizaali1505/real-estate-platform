from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, LeadViewSet, SavedSearchViewSet

router = DefaultRouter()
router.register(r'properties', PropertyViewSet, basename='property')
router.register(r'leads', LeadViewSet, basename='lead')
router.register(r'saved-searches', SavedSearchViewSet, basename='savedsearch')


urlpatterns = [
    path('', include(router.urls)),
]



