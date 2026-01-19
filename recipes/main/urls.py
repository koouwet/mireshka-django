from rest_framework.routers import DefaultRouter
from .views import (
    RecipeViewSet,
    IngridientsViewSet,
    InstructionViewSet,
    TagsViewSet,
    FavouriteViewSet,
)

router = DefaultRouter()
router.register("recipes", RecipeViewSet)
router.register("ingridients", IngridientsViewSet)
router.register("instruction", InstructionViewSet)
router.register("tags", TagsViewSet)
router.register("favourite", FavouriteViewSet)

urlpatterns = router.urls
