from django.conf.urls.static import static

from money_manage_Django.Transactions.models import *


MODELS = {
    'statuses': Status,
    'types': Type,
    'categories': Category,
    'subcategories': Subcategory,
}
