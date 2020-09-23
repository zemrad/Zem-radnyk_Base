from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views.generic import ListView, View, UpdateView, FormView
from .models import Order, Profile, Kadastr_Number
from .forms import DirectorForm, KadastrNumberForm
from datetime import timedelta
from django.contrib.auth.decorators import login_required

from django.db.models import Q


# Create your views here.

class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, template_name='index.html')
        else:
            return redirect('login')


class SearchView(View):
    def post(self, request):
        search = request.POST['search']
        return redirect('search_result', search)


class SearchResultView(View):
    def get(self, request, slug):
        if request.user.is_authenticated:
            orders = Order.objects.filter(
                Q(order_number__contains=slug) | Q(kadastr_number__contains=slug) |
                Q(pib__contains=slug) | Q(ipn__contains=slug) | Q(pasport__contains=slug) |
                Q(sovet__contains=slug) | Q(contact__contains=slug)
            )
            return render(request, 'search_detail.html', {'orders': orders})
        else:
            return redirect('login')


class DirectorView(View):
    def get(self, request):
        if request.user.is_authenticated:
            orders = Order.objects.all
            return render(request, 'orders.html', {'orders': orders})
        else:
            return redirect('login')


class DirectorFormView(View):
    form_class = DirectorForm
    initial = {'key': 'value'}
    template_name = 'add_kontrakt.html'

    def get(self, request):
        if request.user.is_authenticated:
            form = self.form_class(initial=self.initial)
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('login')

    def post(self, request):
        form = DirectorForm(request.POST)
        user = get_object_or_404(Profile, user=request.user.id)
        if form.is_valid():

            order = form.save(commit=False)
            if user.orderer:
                order.orderer = user.orderer
            if order.first_session_response_date != None:
                order.first_session_response_date_plus_30_days = order.first_session_response_date + timedelta(days=30)
                print(order.first_session_response_date)
            if (order.sending_response_date_zatverg != None):
                order.sending_response_date_zatverg_plus_14_days = order.sending_response_date_zatverg + timedelta(
                    days=14)
            order.order_number += request.POST['code_of_kadastr_number']
            order.save()
        return redirect('/')


class DirectorEditView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            order = get_object_or_404(Order, order_number=kwargs.get('slug'))
            form = DirectorForm(instance=order)
            return render(request, 'edit_order.html', context={'form': form})
        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, order_number=kwargs.get('slug'))
        form = DirectorForm(request.POST, instance=order)

        order_from_form = form.save(commit=False)

        if order_from_form.first_session_response_date != None:
            order.first_session_response_date_plus_30_days = order.first_session_response_date + timedelta(days=30)
        if order_from_form.sending_response_date_zatverg != None:
            order.sending_response_date_zatverg_plus_14_days = order.sending_response_date_zatverg + timedelta(days=14)

        com = form.save()

        return redirect('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = get_object_or_404(Order, order_number=kwargs.get('slug'))
        return context


class KadastrNumberView(ListView):
    model = Kadastr_Number
    context_object_name = 'kadastr_numbers'
    template_name = 'kadastr_base.html'




class PeopleOnCadastrNumber(View):

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_authenticated and request.user.orderer.role != 'zamovnik':
                people = Order.objects.all().filter(kadastr_number=kwargs['slug'])
                return render(request, 'people_on_kadastr_number.html', context={'people': people})
            else:
                return render(request, 'access_error.html')
        else:
            return redirect('login')


class AddKadastrNumber(View):

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_authenticated and request.user.orderer.role != 'zamovnik':
                form = KadastrNumberForm()
                return render(request, 'add_kadastr_number.html', context={'form': form})
            else:
                return render(request, 'access_error.html')
        else:
            return redirect('login')


    def post(self, request):
        form = KadastrNumberForm(request.POST)
        if form.is_valid():
            kadastr_number_from_form = form.save()
        return redirect('kadastr_numbers')
