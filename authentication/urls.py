from django.conf.urls import url, include, patterns
from django.contrib import admin

from rest_framework import routers

from authentication.views import GroupViewSet
from authentication.views import UserViewSet
# from authentication.views import register_by_access_token


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^admin/', include(admin.site.urls)),
)