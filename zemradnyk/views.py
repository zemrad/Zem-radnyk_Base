from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views.generic import ListView, View, UpdateView, FormView
from .models import Order, Profile, Kadastr_Number, Oblast, Orderer, Rayon, Otg
from .forms import DirectorForm, KadastrNumberForm
from datetime import timedelta
from django.http import FileResponse
from num2words import num2words
import os
from docxtpl import DocxTemplate


from django.db.models import Q


# Create your views here.

def get_orderer():
    return Orderer.objects.all()


def get_rayon():
    return Rayon.objects.all()


def get_oblast():
    return Oblast.objects.all()


def get_otg():
    return Otg.objects.all()


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
                Q(sovet__contains=slug) | Q(contact__contains=slug) | Q(orderer__name__contains=slug)
            )
            return render(request, 'search_detail.html', {'orders': orders})
        else:
            return redirect('login')


class DirectorView(View):
    def get(self, request):
        if request.user.is_authenticated:
            orders = Order.objects.all().order_by('order_date')
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
        form = DirectorForm(request.POST, request.FILES)
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
            order.who_added = request.user.username
            order.save()

        return redirect('detail', request.POST['order_number'])


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
        form = DirectorForm(request.POST, request.FILES, instance=order)

        order_from_form = form.save(commit=False)

        if order_from_form.first_session_response_date != None:
            order.first_session_response_date_plus_30_days = order.first_session_response_date + timedelta(days=30)
        if order_from_form.sending_response_date_zatverg != None:
            order.sending_response_date_zatverg_plus_14_days = order.sending_response_date_zatverg + timedelta(days=14)

        global fp
        global sp
        global tp
        a = list()

        if order_from_form.first_payment != None:
            fp = int(order_from_form.first_payment)
            a.append(fp)
        if order_from_form.second_payment != None:
            sp = int(order_from_form.second_payment)
            a.append(sp)
        if order_from_form.third_payment != None:
            tp = int(order_from_form.third_payment)
            a.append(tp)

        summa = 0
        for i in a:
            summa += i

        order.payed = summa
        order.who_edit += request.user.username + ', '
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
    queryset = Kadastr_Number.objects.order_by('-id')
    extra_context = {'orderers': get_orderer(),
                     'rayons': get_rayon(),
                     'regions': get_oblast(),
                     'otgs': get_otg()}



class PeopleOnCadastrNumber(View):

    def get(self, request, **kwargs):
        if request.user.is_authenticated:

                people = Order.objects.all().filter(kadastr_number=kwargs['slug']).order_by('number_of_location')
                kadastr_number = get_object_or_404(Kadastr_Number, kadastr_number=kwargs['slug'])
                return render(request, 'people_on_kadastr_number.html', context={'people': people, 'kadastr_number': kadastr_number})

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


class PeopleZamovnik(View):

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_authenticated and request.user.orderer.role != 'zamovnik':
                orders = Order.objects.all().filter(orderer__name=kwargs['slug'])
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
        form = KadastrNumberForm(request.POST, request.FILES)
        if form.is_valid():

            kadastr_number_from_form = form.save(commit=False)
            kadastr_number_from_form.who_added = request.user.username
            kadastr_number_from_form.save()
        return redirect('kadastr_numbers')

class EditKadastrNumber(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
                kadastr_number = get_object_or_404(Kadastr_Number, kadastr_number=kwargs['slug'])
                form = KadastrNumberForm(instance=kadastr_number)
                return render(request, 'add_kadastr_number.html', context={'form': form})

        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        kadastr_number = get_object_or_404(Kadastr_Number, kadastr_number=kwargs['slug'])
        form = KadastrNumberForm(request.POST, request.FILES, instance=kadastr_number)
        if form.is_valid():
            kadastr_number_from_form = form.save(commit=False)
            kadastr_number_from_form.who_edit += request.user.username + ', '
            kadastr_number_from_form.save()
        return redirect('kadastr_numbers')


class MakeKontrakt(View):

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            order = get_object_or_404(Order, order_number=kwargs['slug'])
            import os
            THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
            my_file = os.path.join(THIS_FOLDER, 'text.docx')
            doc = DocxTemplate(my_file)
            total_text = ''
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


            pib = order.pib.split(" ")
            pib_small = ''
            for i in pib[1:]:
                pib_small += i[0] + '. '
            pib_small += pib[0]

            context = {'order_number': order.order_number, 'order_date': order.order_date.strftime('%d.%m.%Y'),
                       'total': order.total, 'total_text': total_text, 'pib': order.pib, 'ipn': order.ipn,
                       'contact': order.contact, 'pasport': order.pasport, 'pib_small': pib_small, 'rayon': order.rayon, 'rada': order.sovet}
            doc.render(context)
            doc.save("Договор № {}.docx".format(order.order_number))
            file = open("Договор № {}.docx".format(order.order_number), 'rb')

            response = FileResponse(file)
            os.remove("Договор № {}.docx".format(order.order_number))
            return response
        else:
            return redirect('login')


class OblastView(ListView):
    template_name = 'oblast.html'
    model = Oblast
    context_object_name = 'oblast_list'


class RayonInOblast(View):

    def get(self, request, *args, **kwargs):
        kadastr_numbers = Kadastr_Number.objects.filter(rayon__name=kwargs['slug'])
        return render(request, 'kadastr_base.html', {'kadastr_numbers': kadastr_numbers,
                                                     'orderers': get_orderer(),
                                                     'rayons': get_rayon(),
                                                     'regions': get_oblast(),
                                                     'otgs': get_otg()})


class VitagView(View):
     def get(self, request, *args, **kwargs):
         kadastr_numbers = Kadastr_Number.objects.filter(vitag=True)
         return render(request, 'kadastr_base.html', {'kadastr_numbers': kadastr_numbers,
                                                     'orderers': get_orderer(),
                                                     'rayons': get_rayon(),
                                                     'regions': get_oblast(),
                                                     'otgs': get_otg()})


class RazbivkaView(View):
    def get(self, request, *args, **kwargs):
        kadastr_numbers = Kadastr_Number.objects.filter(to_razbivka=True)
        return render(request, 'kadastr_base.html', {'kadastr_numbers': kadastr_numbers,
                                                     'orderers': get_orderer(),
                                                     'rayons': get_rayon(),
                                                     'regions': get_oblast(),
                                                     'otgs': get_otg()})


class KadastrOrderersView(View):
    def get(self, request, *args, **kwargs):
        kadastr_numbers = Kadastr_Number.objects.filter(reserv__name=kwargs['slug'])
        return render(request, 'kadastr_base.html', {'kadastr_numbers': kadastr_numbers,
                                                     'orderers': get_orderer(),
                                                     'rayons': get_rayon(),
                                                     'regions': get_oblast(),
                                                     'otgs': get_otg()})


class KadastrRayonView(View):
    def get(self, request, *args, **kwargs):
        kadastr_numbers = Kadastr_Number.objects.filter(rayon__name=kwargs['slug'])
        return render(request, 'kadastr_base.html', {'kadastr_numbers': kadastr_numbers,
                                                     'orderers': get_orderer(),
                                                     'rayons': get_rayon(),
                                                     'regions': get_oblast(),
                                                     'otgs': get_otg()})


class VRobotiView(View):
    def get(self, request, *args, **kwargs):
        kadastr_numbers = Kadastr_Number.objects.filter(in_work=kwargs['slug'])
        return render(request, 'kadastr_base.html', {'kadastr_numbers': kadastr_numbers,
                                                     'orderers': get_orderer(),
                                                     'rayons': get_rayon(),
                                                     'regions': get_oblast(),
                                                     'otgs': get_otg()})


class KadastrOblastView(View):
    def get(self, request, *args, **kwargs):
        kadastr_numbers = Kadastr_Number.objects.filter(oblast__name=kwargs['slug'])
        return render(request, 'kadastr_base.html', {'kadastr_numbers': kadastr_numbers,
                                                     'orderers': get_orderer(),
                                                     'rayons': get_rayon(),
                                                     'regions': get_oblast(),
                                                     'otgs': get_otg()})

class KadastrOtgView(View):
    def get(self, request, *args, **kwargs):
        kadastr_numbers = Kadastr_Number.objects.filter(otg__name=kwargs['slug'])
        return render(request, 'kadastr_base.html', {'kadastr_numbers': kadastr_numbers,
                                                     'orderers': get_orderer(),
                                                     'rayons': get_rayon(),
                                                     'regions': get_oblast(),
                                                     'otgs': get_otg()})


class KNSearchView(View):
    def post(self, request):
        search = request.POST['search']
        return redirect('knsearch_result', search)


class KNSearchResultView(View):
    def get(self, request, slug):
        if request.user.is_authenticated:

            people = Order.objects.filter(kadastr_number=slug).order_by('number_of_location')
            kadastr_number = get_object_or_404(Kadastr_Number, kadastr_number=slug)
            return render(request, 'people_on_kadastr_number.html',
                          context={'people': people, 'kadastr_number': kadastr_number})
        else:
            return redirect('login')






