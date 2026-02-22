from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, ContactViewSet, DocumentViewSet

router = DefaultRouter()
router.register(r'jobs', JobViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'documents', DocumentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]