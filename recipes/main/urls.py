from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet, IngridientsViewSet, InstructionViewSet, TagsViewSet, FavouriteViewSet

router = DefaultRouter()
router.register("recipes", RecipeViewSet, basename='recipes')
router.register("ingridients", IngridientsViewSet, basename='ingridients')
router.register("instruction", InstructionViewSet, basename='instruction')
router.register("tags", TagsViewSet, basename='tags')
router.register("favourite", FavouriteViewSet, basename='favourite')
urlpatterns = router.urls
