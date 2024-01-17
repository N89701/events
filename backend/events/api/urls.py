from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EventViewSet, OrganizationViewSet

router_v1 = DefaultRouter()
router_v1.register('organizations', OrganizationViewSet, basename='organizations')
router_v1.register('events', EventViewSet, basename='events')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
]
