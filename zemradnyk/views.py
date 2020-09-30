from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views.generic import ListView, View, UpdateView, FormView
from .models import Order, Profile, Kadastr_Number
from .forms import DirectorForm, KadastrNumberForm
from datetime import timedelta
from django.http import FileResponse
from num2words import num2words
from babel.dates import format_date


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


class OrderDetail(View):
    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            order = get_object_or_404(Order, order_number=kwargs['slug'])
            return render(request, 'detail.html', {'order': order})
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
        return redirect('detail', order.order_number)


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

        return redirect('detail', order.order_number)

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


class PeopleOnRayon(View):

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_authenticated and request.user.orderer.role != 'zamovnik':
                orders = Order.objects.all().filter(rayon__name=kwargs['slug'])
                return render(request, 'orders.html', context={'orders': orders})
            else:
                return render(request, 'access_error.html')
        else:
            return redirect('login')


class PeopleRozrobnik(View):

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_authenticated and request.user.orderer.role != 'zamovnik':
                orders = Order.objects.all().filter(developer__name=kwargs['slug'])
                return render(request, 'orders.html', context={'orders': orders})
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


class MakeKontrakt(View):

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            order = get_object_or_404(Order, order_number=kwargs['slug'])
            from docxtpl import DocxTemplate
            doc = DocxTemplate('static/text.docx')

            if order.total != None:
                total_text = num2words(order.total, lang='uk')

                if total_text[-2:] == 'на':
                    total_text += " гривня 00 копійок"
                elif total_text[-2:] == 'вi':
                    total_text += ' гривні 00 копійок'
                elif total_text[-2:] == 'ри':
                    total_text += ' гривні 00 копійок'
                else:
                    total_text += ' гривень 00 копійок'
                total = float(order.total)

            pib = order.pib.split(" ")
            pib_small = ''
            for i in pib[0:2]:
                pib_small += i[0] + '. '
            pib_small += pib[2]

            context = {'order_number': order.order_number, 'order_date': order.order_date.strftime('%d.%m.%Y'),
                       'total': total, 'total_text': total_text, 'pib': order.pib, 'ipn': order.ipn,
                       'contact': order.contact, 'pasport': order.pasport, 'pib_small': pib_small, 'rayon': order.rayon, 'rada': order.sovet}
            doc.render(context)
            doc.save("Договор № {}.docx".format(order.order_number))
            file = open("Договор № {}.docx".format(order.order_number), 'rb')

            response = FileResponse(file)
            return response
        else:
            return redirect('login')
