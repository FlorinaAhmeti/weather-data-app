from rest_framework.routers import DefaultRouter
from .viewsets import BulgarianMeteoProDataViewSet

router = DefaultRouter()
router.register(r'bulgarian-metoe-pro', BulgarianMeteoProDataViewSet, basename='bulgarian-metoe-pro')

urlpatterns = router.urls
