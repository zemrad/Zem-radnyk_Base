
from django.urls import path
from .views import IndexView, SearchView, SearchResultView, DirectorFormView, DirectorView, DirectorEditView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search', SearchView.as_view(), name='search'),
    path('search/<slug:slug>', SearchResultView.as_view(), name='search_result'),
    path('orders/add', DirectorFormView.as_view(), name='add_order'),
    path('orders', DirectorView.as_view(), name='order_list'),
    path('orders/edit/<slug:slug>', DirectorEditView.as_view(), name='order_edit'),
]