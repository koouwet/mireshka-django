from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status

from .models import Recipe, Ingridients, Favourite


class RecipeTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="12345"
        )

        self.token = Token.objects.create(user=self.user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

    def test_recipe_create_success(self):

        """
        Проверяет успешное создание рецепта.
        """

        data = {
            "title": "Блины",
            "description": "Очень вкусные",
            "cooking_time": 20,
            "servings": 4,
            "difficulty": "easy",
            "kitchen": "русская"
        }

        response = self.client.post(
            "/api/recipes/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        recipe = Recipe.objects.get(title="Блины")

        self.assertEqual(
            recipe.author,
            self.user
        )



    def test_recipe_negative_cooking_time(self):
        """
        Проверяет запрет отрицательного времени приготовления.
        """

        data = {
            "title": "Плохой рецепт",
            "description": "Очень плохой рецепт",
            "cooking_time": -10,
            "servings": 4,
            "difficulty": "easy",
            "kitchen": "русская"
        }

        response = self.client.post(
            "/api/recipes/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertIn(
            "cooking_time",
            response.data
        )

    def test_recipe_negative_servings(self):
        """
        Проверяет запрет отрицательного количества порций.
        """

        data = {
            "title": "Плохой рецепт",
            "description": "Очень плохой рецепт",
            "cooking_time": 20,
            "servings": -1,
            "difficulty": "easy",
            "kitchen": "русская"
        }

        response = self.client.post(
            "/api/recipes/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertIn(
            "servings",
            response.data
        )

    def test_filter_by_difficulty(self):
        """
        Проверяет фильтрацию рецептов по сложности.
        """

        Recipe.objects.create(
            title="Яичница",
            description="Тест",
            cooking_time=10,
            servings=1,
            difficulty="easy",
            kitchen="русская",
            author=self.user
        )

        Recipe.objects.create(
            title="Карбонара",
            description="Тест",
            cooking_time=30,
            servings=4,
            difficulty="medium",
            kitchen="итальянская",
            author=self.user
        )

        response = self.client.get(
            "/api/recipes/?difficulty=easy"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            1
        )

        self.assertEqual(
            response.data["results"][0]["difficulty"],
            "easy"
        )

    def test_filter_by_kitchen(self):
        """
        Проверяет фильтрацию рецептов по кухне.
        """

        Recipe.objects.create(
            title="Борщ",
            description="Тест",
            cooking_time=60,
            servings=4,
            difficulty="easy",
            kitchen="русская",
            author=self.user
        )

        Recipe.objects.create(
            title="Карбонара",
            description="Тест",
            cooking_time=30,
            servings=4,
            difficulty="medium",
            kitchen="итальянская",
            author=self.user
        )

        response = self.client.get(
            "/api/recipes/?kitchen=русская"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            1
        )

        self.assertEqual(
            response.data["results"][0]["kitchen"],
            "русская"
        )


    def test_search_recipe(self):
        """
        Проверяет поиск рецептов.
        """

        Recipe.objects.create(
            title="Гороховый суп",
            description="Очень вкусный",
            cooking_time=60,
            servings=4,
            difficulty="easy",
            kitchen="русская",
            author=self.user
        )

        Recipe.objects.create(
            title="Карбонара",
            description="Паста",
            cooking_time=30,
            servings=4,
            difficulty="medium",
            kitchen="итальянская",
            author=self.user
        )

        response = self.client.get(
            "/api/recipes/?search=суп"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            1
        )

        self.assertIn(
            "суп",
            response.data["results"][0]["title"].lower()
        )

    def test_ordering_by_cooking_time(self):
        """
        Проверяет сортировку рецептов по времени приготовления.
        """

        Recipe.objects.create(
            title="Долгий",
            description="Тест",
            cooking_time=90,
            servings=4,
            difficulty="easy",
            kitchen="русская",
            author=self.user
        )

        Recipe.objects.create(
            title="Быстрый",
            description="Тест",
            cooking_time=10,
            servings=4,
            difficulty="easy",
            kitchen="русская",
            author=self.user
        )

        response = self.client.get(
            "/api/recipes/?ordering=cooking_time"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertLessEqual(
            response.data["results"][0]["cooking_time"],
            response.data["results"][1]["cooking_time"]
        )    


    def test_by_difficulty_action(self):
        """
        Проверяет работу action для группировки по сложности.
        """

        Recipe.objects.create(
            title="Яичница",
            description="Тест",
            cooking_time=10,
            servings=1,
            difficulty="easy",
            kitchen="русская",
            author=self.user
        )

        Recipe.objects.create(
            title="Карбонара",
            description="Тест",
            cooking_time=30,
            servings=4,
            difficulty="medium",
            kitchen="итальянская",
            author=self.user
        )

        response = self.client.get(
            "/api/recipes/by_difficulty/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIn("easy", response.data)
        self.assertIn("medium", response.data)
        self.assertIn("hard", response.data)


    def test_scale_recipe(self):
        """
        Проверяет масштабирование ингредиентов рецепта.
        """

        recipe = Recipe.objects.create(
            title="Яичница",
            description="Тест",
            cooking_time=10,
            servings=2,
            difficulty="easy",
            kitchen="русская",
            author=self.user
        )

        ingredient = Ingridients.objects.create(
            recipe=recipe,
            name="Яйцо",
            quantity=2,
            unit="шт"
        )

        response = self.client.post(
            f"/api/recipes/{recipe.id}/scale/",
            {
                "servings": 4
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        ingredient.refresh_from_db()

        self.assertEqual(
            ingredient.quantity,
            4
        )


    def test_is_favourite_context(self):
        """
        Проверяет передачу данных через context.
        """

        recipe = Recipe.objects.create(
            title="Борщ",
            description="Тест",
            cooking_time=60,
            servings=4,
            difficulty="easy",
            kitchen="русская",
            author=self.user
        )

        favourite = Favourite.objects.create(
            user=self.user
        )

        favourite.recipes.add(recipe)

        response = self.client.get(
            "/api/recipes/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertTrue(
            response.data["results"][0]["is_favourite"]
        )    
