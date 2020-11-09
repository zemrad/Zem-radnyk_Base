from django.urls import path
from .views import IndexView, SearchView, SearchResultView, DirectorFormView, DirectorView, DirectorEditView,\
    KadastrNumberView, PeopleOnCadastrNumber, AddKadastrNumber, PeopleOnRayon, PeopleRozrobnik, MakeKontrakt,\
    OrderDetail, EditKadastrNumber, PeopleZamovnik, OblastView, RayonInOblast, VitagView, RazbivkaView, KadastrOrderersView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search', SearchView.as_view(), name='search'),
    path('result/<slug>', SearchResultView.as_view(), name='search_result'),
    path('orders/add', DirectorFormView.as_view(), name='add_order'),
    path('orders', DirectorView.as_view(), name='order_list'),
    path('orders/edit/<slug:slug>', DirectorEditView.as_view(), name='order_edit'),
    path('kadastr-numbers', KadastrNumberView.as_view(), name='kadastr_numbers'),
    path('kadastr-numbers/<slug>/', PeopleOnCadastrNumber.as_view(), name='people_on_kadastr_numbers'),
    path('kadastr-numbers/edit/<slug>/', EditKadastrNumber.as_view(), name='edit_kadastr_number'),
    path('add/kadastr-numbers', AddKadastrNumber.as_view(), name='add_kadastr_numbers'),
    path('rayon/orders/<slug>', PeopleOnRayon.as_view(), name='rayon'),
    path('rozrobnik/orders/<slug>', PeopleRozrobnik.as_view(), name='rozrobnik'),
    path('zamovnik/orders/<slug>', PeopleZamovnik.as_view(), name='zamovnik'),
    path('document/<slug>', MakeKontrakt.as_view(), name='document'),
    path('detail/<slug>', OrderDetail.as_view(), name='detail'),
    path('oblast/', OblastView.as_view(), name='oblast'),
    path('oblast/<slug>', RayonInOblast.as_view(), name='rayon_in_oblast'),
    path('vitag', VitagView.as_view(), name='vitag'),
    path('razbivka', RazbivkaView.as_view(), name='razbivka'),
    path('orderers/<slug>', KadastrOrderersView.as_view(), name='orderers')

]
