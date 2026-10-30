from rest_framework.routers import DefaultRouter

from .views import CategoriaViewSet, MaterialViewSet, ProductoViewSet


router = DefaultRouter()
router.register('categorias', CategoriaViewSet, basename='categoria')
router.register('materiales', MaterialViewSet, basename='material')
router.register('productos', ProductoViewSet, basename='producto')

urlpatterns = router.urls