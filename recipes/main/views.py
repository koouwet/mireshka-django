from rest_framework.viewsets import ModelViewSet
from .models import Recipe, Ingridients, Instruction, Tags, Favourite
from .serializers import RecipeSerializer, IngridientsSerializer, InstructionSerializer, TagsSerializer, FavouriteSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.db.models import Q





class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    ]
    filterset_fields = ["difficulty","kitchen","cooking_time","servings" ]
    ordering_fields = ["created_at","cooking_time","title"]
    search_fields = ["title", "description",]

    @action(methods=["GET"], detail=False)
    def by_difficulty(self, request):

        easy = Recipe.objects.filter(difficulty="easy")
        medium = Recipe.objects.filter(difficulty="medium")
        hard = Recipe.objects.filter(difficulty="hard")

        return Response({
            "easy": RecipeSerializer(easy, many=True).data,
            "medium": RecipeSerializer(medium, many=True).data,
            "hard": RecipeSerializer(hard, many=True).data,
        })

    @action(methods=["POST"], detail=True)
    def scale(self, request, pk=None):
        recipe = self.get_object()

    # используем существующий RecipeSerializer для валидации
        serializer = self.get_serializer(
            recipe,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        new_servings = serializer.validated_data.get("servings")
        old_servings = recipe.servings

        if not new_servings:
            return Response(
                {"detail": "Нужно указать количество порций"},
                status=status.HTTP_400_BAD_REQUEST
            )

        factor = new_servings / old_servings

    # пересчитываем ингредиенты
        for ingredient in recipe.Ingridients.all():
            ingredient.quantity = ingredient.quantity * factor
            ingredient.save()

        recipe.servings = new_servings
        recipe.save()

    # сериализуем обновлённые ингредиенты
        ingridients_data = IngridientsSerializer(
            recipe.Ingridients.all(),
            many=True
        ).data

        return Response(
            {
                "detail": "Рецепт масштабирован",
                "info": "Ингредиенты обновились",
                "old_servings": old_servings,
                "new_servings": new_servings,
                "ingridients": ingridients_data,
            },
            status=status.HTTP_200_OK
        )

                                       
    
    @action(methods=["GET"], detail=False)
    def q_first(self, request):

        recipes = Recipe.objects.filter(
            (Q(difficulty="easy") & Q(cooking_time__lte=30))
            |
            (Q(difficulty="medium") & ~Q(kitchen__iexact="итальянская"))
        )

        serializer = self.get_serializer(recipes, many=True)
        return Response(serializer.data)


    @action(methods=["GET"], detail=False)
    def q_second(self, request):

        recipes = Recipe.objects.filter(
            (Q(difficulty="hard") & Q(servings__gte=4))
            |
            (Q(difficulty="easy") & ~Q(kitchen__iexact="русская"))
        )

        serializer = self.get_serializer(recipes, many=True)
        return Response(serializer.data)
    
    



    

class IngridientsViewSet(ModelViewSet):
    queryset = Ingridients.objects.all()
    serializer_class = IngridientsSerializer

    filter_backends = [SearchFilter]
    search_fields = ["name"]

class InstructionViewSet(ModelViewSet):
    queryset = Instruction.objects.all()
    serializer_class = InstructionSerializer

    filter_backends = [SearchFilter]
    search_fields = ["description"]

class TagsViewSet(ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer

    filter_backends = [SearchFilter]
    search_fields = ["name"]

class FavouriteViewSet(ModelViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer

