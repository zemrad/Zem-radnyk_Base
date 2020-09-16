from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View, UpdateView, FormView
from .models import Order, Profile
from .forms import DirectorForm
from datetime import datetime, timedelta
# Create your views here.


class IndexView(View):
    def get(self, request):
        return render(request, template_name='index.html')


class SearchView(View):
    def post(self, request):
        search = request.POST['search']
        return redirect('search_result', search)


class DirectorView(View):
    def get(self, request):
        orders = Order.objects.all
        return render(request, 'orders.html', {'orders': orders})


class SearchResultView(View):
    def get(self, request, slug):
        order = get_object_or_404(Order, order_number=slug)
        return render(request, 'search_detail.html', {'order': order})



class DirectorFormView(View):
    form_class = DirectorForm
    initial = {'key': 'value'}
    template_name = 'add_kontrakt.html'

    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

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
    # template_name = 'edit_order.html'
    # form_class = DirectorForm
    #
    # def form_valid(self, form):
    #     form.save()
    #     return super().form_valid(form)
    #
    #
    #
    # def get_context_data(self, **kwargs):
    #
    #     context = super().get_context_data(**kwargs)
    #     print(self.request.GET)
    #     #context['form'] = get_object_or_404(Order, order_number = kwargs['slug'])
    #     return context

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, order_number=kwargs.get('slug'))
        form = DirectorForm(instance=order)
        return render(request, 'edit_order.html', context={'form': form})

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



  #





