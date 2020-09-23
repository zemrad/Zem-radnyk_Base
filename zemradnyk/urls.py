
from django.urls import path
from .views import IndexView, SearchView, SearchResultView, DirectorFormView, DirectorView, DirectorEditView,\
    KadastrNumberView, PeopleOnCadastrNumber, AddKadastrNumber



urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search', SearchView.as_view(), name='search'),
    path('result/<slug>', SearchResultView.as_view(), name='search_result'),
    path('orders/add', DirectorFormView.as_view(), name='add_order'),
    path('orders', DirectorView.as_view(), name='order_list'),
    path('orders/edit/<slug:slug>', DirectorEditView.as_view(), name='order_edit'),
    path('kadastr-numbers', KadastrNumberView.as_view(), name='kadastr_numbers'),
    path('kadastr-numbers/<slug>/', PeopleOnCadastrNumber.as_view(), name='people_on_kadastr_numbers'),
    path('add/kadastr-numbers', AddKadastrNumber.as_view(), name='add_kadastr_numbers'),

]