from import_export import resources, fields
from .models import Recipe

class RecipeResource(resources.ModelResource):
    # кастомное поле для тегов
    tags = fields.Field(column_name="Теги")

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
            "tags",
        )
        export_order = fields

    # -----------------------------
    # 1️⃣ ЧТО ИМЕННО ЭКСПОРТИРУЕМ
    # -----------------------------
    def get_export_queryset(self, request):
        """
        Экспортируем только рецепты, созданные за последние 30 дней
        """
        from django.utils.timezone import now
        from datetime import timedelta

        return Recipe.objects.filter(
            created_at__gte=now() - timedelta(days=30)
        )

    # -----------------------------
    # 2️⃣ КАК ВЫГЛЯДИТ СЛОЖНОСТЬ
    # -----------------------------
    def dehydrate_difficulty(self, recipe):
        """
        Преобразуем код сложности в читаемый текст
        """
        return dict(recipe._meta.get_field("difficulty").choices).get(
            recipe.difficulty,
            recipe.difficulty
        )

    # -----------------------------
    # 3️⃣ КАК ЭКСПОРТИРУЕМ ТЕГИ
    # -----------------------------
    def dehydrate_tags(self, recipe):
        """
        Объединяем теги в одну строку через запятую
        """
        return ", ".join(tag.name for tag in recipe.Tags.all())
