from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from auth_token_app.views import UserViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/me', UserViewSet.as_view({'get': 'me', 'patch': 'me'}), name="user_view_set"),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
]
