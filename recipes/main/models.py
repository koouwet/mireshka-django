from django.contrib.auth.models import User
from django.db import models
from simple_history.models import HistoricalRecords


class Recipe(models.Model):
    title = models.CharField("Название рецепта", max_length=255)
    description = models.TextField("Описание")
    cooking_time = models.PositiveIntegerField("Время приготовления")
    servings = models.PositiveIntegerField("Количество порций")
    difficulty = models.CharField(
        "Сложность",
        max_length=10,
        choices=[('easy', 'Легкий'), ('medium', 'Средний'), ('hard', 'Трудный')],
        default='easy'
    )
    kitchen = models.CharField("Кухня", max_length=100)
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор"
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
    
class Favourite(models.Model):
    name = models.CharField('Название')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    recipes = models.ManyToManyField(Recipe)
    added_at = models.DateTimeField("Добавлено", auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
    

class Ingridients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="Ingridients"
    )
    name = models.CharField("Название")
    quantity = models.PositiveIntegerField("Количество")
    unit = models.CharField("Единица измерения")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"

class Instruction(models.Model):
    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE, related_name='Instruction')
    count_of_steps = models.PositiveIntegerField('Количество шагов')
    description = models.TextField('Описание')

    def __str__(self):
        return self.description
    
    class Meta:
        verbose_name = "Инструкция"
        verbose_name_plural = "Инструкции"

class Tags(models.Model):
    recipes = models.ManyToManyField(Recipe, related_name="Tags")
    name = models.CharField("Имя")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"   




