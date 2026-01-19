from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from .models import Recipe, Ingridients, Instruction, Tags, Favourite


# ---------- User ----------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


# ---------- Ingridients ----------
class IngridientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingridients
        fields = ("id", "recipe", "name", "quantity", "unit")

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Количество должно быть больше нуля"
            )
        return value


# ---------- Instruction ----------
class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = ("id", "recipe", "count_of_steps", "description")

    def validate_count_of_steps(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Количество шагов не может быть меньше нуля"
            )
        return value


# ---------- Tags ----------
class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ("id", "name", "recipes")


# ---------- Recipe ----------
class RecipeSerializer(serializers.ModelSerializer):

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


        )
        read_only_fields = ("created_at",)

    # -------- ВАЛИДАЦИЯ --------
    def validate_cooking_time(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Время приготовления должно быть положительным числом"
            )
        return value

    def validate_servings(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Количество порций должно быть положительным числом"
            )
        return value

    def validate_difficulty(self, value):
        if value not in ("easy", "medium", "hard"):
            raise serializers.ValidationError(
                "Сложность должна быть: easy, medium или hard"
            )
        return value


# ---------- Favourite ----------
class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ("id", "name", "user", "recipes", "added_at")
        read_only_fields = ("added_at",)
