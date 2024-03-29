from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('api.urls')),
    path('chats/', include('chats.urls')),
    
]

schema_view = get_schema_view(
   openapi.Info(
        title="Events API",
        default_version='v1',
        description="Документация для проекта Events",
        contact=openapi.Contact(email="nick0901@list.ru"),
        license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
    name='schema-redoc'),
] 

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
