from rest_framework.routers import DefaultRouter
from .viewsets import StationViewSet

router = DefaultRouter()
router.register(r'stations', StationViewSet, basename='station')

urlpatterns = router.urls
