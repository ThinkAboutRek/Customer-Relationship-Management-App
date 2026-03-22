from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from CRM_Website.api_views import RecordListAPIView, RecordDetailAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("CRM_Website.urls")),
    path('api/records/', RecordListAPIView.as_view(), name='api_records'),
    path('api/records/<int:pk>/', RecordDetailAPIView.as_view(), name='api_record_detail'),
    path('api/token/', obtain_auth_token, name='api_token'),
]