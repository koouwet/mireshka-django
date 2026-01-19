from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Recipe

def recipe_list(request):
    recipes = Recipe.objects.all()

    return render(
        request,
        "recipes/list.html",
        {
            "recipes": recipes
        }
    )

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    return render(
        request,
        "recipes/detail.html",
        {
            "recipe": recipe
        }
    )

@login_required
def recipe_create(request):
    if request.method == "POST":
        Recipe.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            cooking_time=request.POST.get("cooking_time"),
            servings=request.POST.get("servings"),
            difficulty=request.POST.get("difficulty"),
            kitchen=request.POST.get("kitchen"),
            author=request.user,  # 👈 КРИТИЧЕСКИ ВАЖНО
        )
        return redirect("recipe_list")

    return render(
        request,
        "recipes/form.html"
    )

@login_required
def recipe_update(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if recipe.author != request.user:
        return HttpResponseForbidden("Это не ваш рецепт")

    if request.method == "POST":
        recipe.title = request.POST.get("title")
        recipe.description = request.POST.get("description")
        recipe.cooking_time = request.POST.get("cooking_time")
        recipe.servings = request.POST.get("servings")
        recipe.difficulty = request.POST.get("difficulty")
        recipe.kitchen = request.POST.get("kitchen")
        recipe.save()

        return redirect("recipe_detail", pk=recipe.pk)

    return render(
        request,
        "recipes/form.html",
        {
            "recipe": recipe
        }
    )


@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    # 🔒 защита
    if recipe.author != request.user:
        return HttpResponseForbidden("Это не ваш рецепт")

    if request.method == "POST":
        recipe.delete()
        return redirect("recipe_list")

    return render(
        request,
        "recipes/delete.html",
        {
            "recipe": recipe
        }
    )

