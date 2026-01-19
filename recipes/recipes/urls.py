from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from main import html_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # ---------- АВТОРИЗАЦИЯ ----------
    path("login/", auth_views.LoginView.as_view(
        template_name="recipes/login.html"
    ), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # ---------- HTML ----------
path("recipes/", html_views.recipe_list, name="recipe_list"),
path("recipes/<int:pk>/", html_views.recipe_detail, name="recipe_detail"),
path("recipes/add/", html_views.recipe_create, name="recipe_create"),
path("recipes/<int:pk>/edit/", html_views.recipe_update, name="recipe_update"),
path("recipes/<int:pk>/delete/", html_views.recipe_delete, name="recipe_delete"),


    # ---------- API ----------
    path("api/", include("main.urls")),
]
