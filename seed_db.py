from django.core.management.base import BaseCommand
from money_manage_Django.Transactions.models import Status, Type, Category, Subcategory

class Command(BaseCommand):
    help = "Заполняет базу данных начальными значениями"

    def handle(self, *args, **options):
        Status.objects.get_or_create(name="Бизнес")
        Status.objects.get_or_create(name="Личное")
        Status.objects.get_or_create(name="Налог")

        type_income, _ = Type.objects.get_or_create(name="Пополнение")
        type_expense, _ = Type.objects.get_or_create(name="Списание")

        category_finance, _ = Category.objects.get_or_create(
            name="Финансы",
            type=type_income
        )
        Subcategory.objects.get_or_create(name="Криптовалюта", category=category_finance)
        Subcategory.objects.get_or_create(name="Банкинг", category=category_finance)

        category_marketing, _ = Category.objects.get_or_create(
            name="Маркетинг",
            type=type_expense
        )
        Subcategory.objects.get_or_create(name="Farpost", category=category_marketing)
        Subcategory.objects.get_or_create(name="Avito", category=category_marketing)

        category_infra, _ = Category.objects.get_or_create(
            name="Инфраструктура",
            type=type_expense
        )
        Subcategory.objects.get_or_create(name="VPS", category=category_infra)
        Subcategory.objects.get_or_create(name="Proxy", category=category_infra)

        self.stdout.write(self.style.SUCCESS("База данных успешно заполнена!"))