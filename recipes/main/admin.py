from django.contrib import admin
from .models import Recipe, Favourite, Ingridients, Instruction, Tags
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportModelAdmin
from .resources import RecipeResource



class IngridientsInline(admin.TabularInline):
    model = Ingridients
    extra = 1
    fields = ("name", "quantity", "unit")


class InstructionInline(admin.StackedInline):
    model = Instruction
    max_num = 1
    fields = ("count_of_steps", "description")


class TagInline(admin.TabularInline):
    model = Tags.recipes.through
    fields = ("tags",)
    fk_name = "recipe"


@admin.register(Recipe)
class RecipeAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ("id", "title", "difficulty", "kitchen", "created_at")
    list_display_links = ("title",)
    search_fields = ("title", "description")
    list_filter = ("difficulty", "kitchen")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)
    list_per_page = 25
    inlines = [IngridientsInline, InstructionInline, TagInline]
    resource_class = RecipeResource

@admin.register(Ingridients)
class IngridientsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "quantity", "unit", "recipe_link")
    search_fields = ("name", "recipe__title")
    list_filter = ("unit",)
    list_per_page = 25

    @admin.display(description="Рецепт")
    def recipe_link(self, obj):
        return obj.recipe.title if obj.recipe else "—"


@admin.register(Instruction)
class InstructionAdmin(admin.ModelAdmin):
    list_display = ("id", "recipe", "count_of_steps", "short_description")
    search_fields = ("description", "recipe__title")
    list_per_page = 25

    @admin.display(description="Краткое описание")
    def short_description(self, obj):
        txt = (obj.description or "")
        return (txt[:60] + "...") if len(txt) > 60 else txt


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "recipes_count")
    search_fields = ("name",)
    filter_horizontal = ("recipes",)
    list_per_page = 25

    @admin.display(description="Кол-во рецептов")
    def recipes_count(self, obj):
        return obj.recipes.count()


@admin.register(Favourite)
class FavouriteAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    list_display = ("id", "user", "added_at", "recipes_list")
    search_fields = ("user__username", "recipes__title")
    filter_horizontal = ("recipes",)
    readonly_fields = ("added_at",)
    list_per_page = 25

    @admin.display(description="Рецепты в избранном")
    def recipes_list(self, obj):
        return ", ".join([r.title for r in obj.recipes.all()[:8]])
