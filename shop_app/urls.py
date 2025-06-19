from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, ProductViewSet, UserViewSet, LogoutView

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'products', ProductViewSet)
router.register(r'users', UserViewSet)  
router.register(r'logout', LogoutView,basename='logout')


urlpatterns = [
    path('', include(router.urls)),
]