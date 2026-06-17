from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from .models import Recipe, Ingridients, Instruction, Tags, Favourite



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")



class IngridientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingridients
        fields = ("id", "recipe", "name", "quantity", "unit")

    def validate_quantity(self, value: int) -> int:
        if value <= 0:
            raise serializers.ValidationError(
                "Количество должно быть больше нуля"
            )
        return value



class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = ("id", "recipe", "count_of_steps", "description")

    def validate_count_of_steps(self, value: int) -> int:
        if value < 0:
            raise serializers.ValidationError(
                "Количество шагов не может быть меньше нуля"
            )
        return value


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ("id", "name", "recipes")


class RecipeSerializer(serializers.ModelSerializer):

    ingredients_count = serializers.IntegerField(read_only=True)
    is_favourite = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "title",
            "description",
            "cooking_time",
            "servings",
            "difficulty",
            "kitchen",
            "created_at",
            "ingredients_count",
            "is_favourite",
        )
        read_only_fields = ("created_at",)


    
    def get_is_favourite(self, obj: Recipe) -> bool:
        """
        Проверяет, находится ли рецепт в избранном пользователя.
        """
        favourites = self.context.get("favourites", [])
        return obj.id in favourites

   
    def validate_cooking_time(self, value: int) -> int:
        """
        Проверяет корректность времени приготовления.
        """
        if value <= 0:
            raise serializers.ValidationError(
                "Время приготовления должно быть положительным числом"
            )
        return value

    def validate_servings(self, value: int) -> int:
        """
        Проверяет корректность количества порций.
        """
        if value <= 0:
            raise serializers.ValidationError(
                "Количество порций должно быть положительным числом"
            )
        return value

    def validate_difficulty(self, value: str) -> str:
        """
        Проверяет допустимое значение сложности рецепта.
        """
        if value not in ("easy", "medium", "hard"):
            raise serializers.ValidationError(
                "Сложность должна быть: easy, medium или hard"
            )
        return value



class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ("id", "name", "user", "recipes", "added_at")
        read_only_fields = ("added_at",)
