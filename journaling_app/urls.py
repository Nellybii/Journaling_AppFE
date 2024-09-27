
from django.contrib import admin
from django.urls import path, include
from journal.views import userViews
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', userViews.UserRegistrationView.as_view(), name='user-register'),
    path("token/", TokenObtainPairView.as_view(), name="get_token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path('api/', include('journal.urls'))
]
