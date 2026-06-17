from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from .views import (
    RecipeViewSet,
    IngridientsViewSet,
    InstructionViewSet,
    TagsViewSet,
    FavouriteViewSet,
)

router = DefaultRouter()
router.register("recipes", RecipeViewSet, basename='recipes')
router.register("ingridients", IngridientsViewSet)
router.register("instruction", InstructionViewSet)
router.register("tags", TagsViewSet)
router.register("favourite", FavouriteViewSet)

urlpatterns = [
    path("token/", obtain_auth_token),
]

urlpatterns += router.urls
