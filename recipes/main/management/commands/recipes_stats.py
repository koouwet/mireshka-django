from django.core.management.base import BaseCommand
from main.models import Recipe


class Command(BaseCommand):
    help = "Выводит статистику по рецептам"

    def handle(self, *args, **options):
        total = Recipe.objects.count()
        easy = Recipe.objects.filter(difficulty="easy").count()
        medium = Recipe.objects.filter(difficulty="medium").count()
        hard = Recipe.objects.filter(difficulty="hard").count()
        quick = Recipe.objects.filter(cooking_time__lte=30).count()

        self.stdout.write("Статистика рецептов:")
        self.stdout.write(f"Всего рецептов: {total}")
        self.stdout.write(f"Лёгкие: {easy}")
        self.stdout.write(f"Средние: {medium}")
        self.stdout.write(f"Сложные: {hard}")
        self.stdout.write(f"Быстрые (до 30 мин): {quick}")
