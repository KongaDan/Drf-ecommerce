from django.contrib import admin
from django.urls import path, include
from shop.views import  CategoryAPIView,ProductAPIview

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/category/',CategoryAPIView.as_view()),
    path('api/product/',ProductAPIview.as_view()),
]
