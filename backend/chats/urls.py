from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ChatViewSet

router_v1 = DefaultRouter()
router_v1.register('', ChatViewSet, basename='chats')

urlpatterns = [
    path('', include(router_v1.urls)),
]
