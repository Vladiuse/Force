from django.urls import path
from . import views

app_name = 'office'
urlpatterns = [
    path('', views.index, name='index'),
    path('kt_domains', views.kt_domains, name='kt_domains'),
    path('beget_domains', views.beget_domains, name='beget_domains'),
    path('offers', views.offers, name='offers'),
    path('checker/<int:offer_id>/<int:mode>/', views.checker_offer, name='checker_offer'),
    path('url_checker', views.url_checker, name='url_checker'),
    path('requisites', views.code_examples, name='code_examples'),
    path('join-urls', views.join_urls, name='join_urls'),
    path('new-offers', views.new_offers, name='new_offers'),

    path('copy_paste', views.copy_paste, name='copy_paste'),  # получить названия кнопок
    path('copy_paste/code_examples_data', views.code_examples_data),  # получить субкнопки и данные
    path('copy_paste/add_group', views.add_button),  # добавить группу
    path('copy_paste/remove_group', views.remove_button),  # удалить группу
    path('copy_paste/add_sub_button', views.add_sub_button),  # добавить субкнопку
    path('copy_paste/remove_sub_button', views.remove_sub_button),  # удалить субкнопку

    path('update_spend', views.update_spend, name='update_spend'),
    path('domain_spends', views.dom_camps, name='domain_spends'),
]
