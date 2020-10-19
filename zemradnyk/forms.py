from django import forms
from .models import Order, Kadastr_Number
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings


class DirectorForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['order_number', 'order_date', 'pib', 'contact', 'location', 'kadastr_number', 'ipn', 'pasport', 'rayon', 'sovet',
                  'type_of_works', 'orderer', 'exist_mark', 'date', 'sending_date', 'pre_response_date', 'response_date', 'developer',
                  'first_session_date', 'first_session_response_date', 'response_rada', 'oskargenya_1', 'dev_message_mov_zgoda',
                  'oskargenya_2', 'sending_date_zatverg', 'sending_response_date_zatverg', 'oskargenya_zatverg', 'register', 'register_ZD',
                  'vidpovidalny', 'first_date', 'akt_vigotovleno_date', 'akt_pidpisano_date', 'granichniy_complete_date',
                  'complite_date', 'pogodjenya', 'expertise', 'podonya_date', 'number_ZV', 'register', 'total', 'payed',
                  'note', 'sending_response_date_zatverg_plus_14_days', 'first_session_response_date_plus_30_days', 'doverenost' ]

        widgets = {
            'order_date': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'sending_date': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'pre_response_date': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'response_date': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'first_session_date': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'first_session_response_date': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'sending_date_zatverg': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'sending_response_date_zatverg': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'first_date': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'akt_vigotovleno_date': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'akt_pidpisano_date': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'granichniy_complete_date': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'podonya_date': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'complite_date': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'pib': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'ipn': forms.TextInput(attrs={'class': 'form-control'}),
            'pasport': forms.TextInput(attrs={'class': 'form-control'}),
            'rayon': forms.Select(attrs={'class': 'form-control'}),
            'sovet': forms.TextInput(attrs={'class': 'form-control'}),
            'type_of_works': forms.Select(attrs={'class': 'form-control'}),
            'orderer': forms.Select(attrs={'class': 'form-control'}),
            'exist_mark': forms.Select(attrs={'class': 'form-control'}),
            'developer': forms.Select(attrs={'class': 'form-control'}),
            'response_rada': forms.Select(attrs={'class': 'form-control'}),
            'oskargenya_1': forms.TextInput(attrs={'class': 'form-control'}),
            'dev_message_mov_zgoda': forms.TextInput(attrs={'class': 'form-control'}),
            'oskargenya_zatverg': forms.TextInput(attrs={'class': 'form-control'}),
            'register': forms.TextInput(attrs={'class': 'form-control'}),
            'register_ZD': forms.TextInput(attrs={'class': 'form-control'}),
            'vidpovidalny': forms.Select(attrs={'class': 'form-control'}),
            'pogodjenya': forms.TextInput(attrs={'class': 'form-control'}),
            'expertise': forms.TextInput(attrs={'class': 'form-control'}),
            'number_ZV': forms.TextInput(attrs={'class': 'form-control'}),
            'total': forms.TextInput(attrs={'class': 'form-control'}),
            'payed': forms.TextInput(attrs={'class': 'form-control'}),
            'oskargenya_2': forms.TextInput(attrs={'class': 'form-control'}),
            'kadastr_number': forms.TextInput(attrs={'class': 'form-control'}),
            'order_number': forms.TextInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control'}),
            'doverenost': forms.Select(attrs={'class': 'form-control'})
        }
        date_geodeziya = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)


class KadastrNumberForm(forms.ModelForm):

    class Meta:
        model = Kadastr_Number
        fields = ('kadastr_number', 'reserv', 'in_work')
        widgets = {
            'kadastr_number': forms.TextInput(attrs={'class': 'form-control'}),
            'reserv': forms.TextInput(attrs={'class': 'form-control'}),
            'in_work': forms.Select(attrs={'class': 'form-control'})
        }


class UserLoginForm(AuthenticationForm):
     def __init__(self, *args, **kwargs):
         super(UserLoginForm, self).__init__(*args, **kwargs)

     username = forms.CharField(widget=forms.TextInput(
         attrs={'class': 'form-control', 'placeholder': 'Логин', 'id': 'hello'}))
     password = forms.CharField(widget=forms.PasswordInput(
         attrs={
             'class': 'form-control',
             'placeholder': 'Пароль',
             'id': 'hi',
         }
 ))