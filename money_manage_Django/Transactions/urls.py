from django.urls import path, re_path


from .views import *


urlpatterns= [
    path('', record_list, name='record_list'),
]

#     path('  home/', index, name='home'), #http://127.0.0.1:8000/Armia
#     path('cats/<int:catid>/', categories), #http://127.0.0.1:8000/categories
#     #path('tables/', tables)
#     path('tables/<str:table_name>/', tables, name='tables'),
#     #path('edit_weaponModel/<int:weaponModel_id>/', edit_weaponModel, name='edit_weaponModel'),
#     path('tables/WeaponModel/', tables, name='tables_WeaponModel'),
#     path('add_item/<str:table_name>/', add_item, name='add_item'),
#     path('delete_item/<str:table_name>/<str:item_id>/', delete_item, name='delete_item'),
#     #path('redact/<str:table_name>/<str:item_id>/', edit_item, name='edit_item'),
#     path('redact/<str:table_name>/<str:item_id>/', edit_item, name='edit_item'),
#     path('generate_report/', report_view, name='generate_report'),
#     path('generate_excel/', generate_excel_report, name='generate_excel'),
#     path('generate_docx/', generate_docx_report, name='generate_docx'),
#     path('ws/some_path/', consumers.YourWebSocketConsumer.as_asgi()),
#     path('', home_view, name='home'),
#     #re_path(r'^tables/(?P<year>[0-9]{4})/',tables),