from rest_framework.routers import DefaultRouter
from .viewsets import BulgarianMeteoProDataViewSet

router = DefaultRouter()
router.register(r'bulgarian_metoe_pro', BulgarianMeteoProDataViewSet, basename='bulgarian_metoe_pro')

urlpatterns = router.urls
