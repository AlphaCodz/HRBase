from django.urls import re_path, path, include
from django.contrib import admin
from rest_framework import permissions, routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from entity.views.authentication import SignUpUser, SignInUserView, CustomTokenBlacklistView
from organisation.views.primary_views import OrganisationViewSet
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenBlacklistView


schema_view = get_schema_view(
    openapi.Info(
        title="HRBase API",
        default_version='v1',
        description="HR Base is a software application that brings job seekers and employers together. It allows companies to post vacancies(jobs) while enabling job seekers to apply for these vacancies.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register('signup', SignUpUser, basename='signup')
router.register('org/create', OrganisationViewSet, basename='organisation')

urlpatterns = [
    path('youshouldnotbeherechief/', admin.site.urls),
    path('api/', include(router.urls)),
    path('login/', SignInUserView.as_view(), name='login-user'),
    path('api/token/blacklist/', CustomTokenBlacklistView.as_view(), name='token_blacklist'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]

