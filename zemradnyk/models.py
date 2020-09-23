from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Orderer(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Vipovilny(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Kadastr_Number(models.Model):
    kadastr_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.kadastr_number


class TypeWork(models.Model):
    type_of_work = models.CharField(max_length=50)

    def __str__(self):
        return self.type_of_work


class Rozrobnik(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='orderer', on_delete=models.CASCADE)
    orderer = models.ForeignKey(Orderer, on_delete=models.CASCADE, blank=True, null=True)
    role = models.CharField(max_length=30, blank=True, null=True)


class Rayon(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_number = models.CharField(max_length=100, unique=True)
    order_date = models.DateField()
    pib = models.CharField(max_length=250)
    contact = models.CharField(max_length=10)
    location = models.CharField(max_length=250)
    kadastr_number = models.CharField(max_length=300, blank=True, null=True)
    ipn = models.CharField(max_length=50)
    pasport = models.CharField(max_length=25)
    rayon =  models.ForeignKey(Rayon, on_delete=models.CASCADE)
    sovet = models.CharField(max_length=150)
    type_of_works = models.ForeignKey(TypeWork, on_delete=models.CASCADE, blank=True, null=True)
    orderer = models.ForeignKey(Orderer, on_delete=models.CASCADE, blank=True, null=True)
    #geodeziya
    MARK_CHOICES = (
        ('✓', '✓'),
        ('✕', '✕')
    )
    exist_mark = models.CharField(default='✕', max_length=10, choices=MARK_CHOICES, blank=True, null=True)
    date = models.DateField(blank=True, null=True,)

    #rozrobnyk
    developer = models.ForeignKey(Rozrobnik, on_delete=models.CASCADE, related_name='developer', blank=True, null=True)
    #law
    RESPONSE_RADA_CHOISE = (
        ('Дозвіл', 'Дозвіл'),
        ('Не розглянуто протягом 1 міс.', 'Не розглянуто протягом 1 міс.'),
        ('Відмова', 'Відмова')
    )
    sending_date = models.DateField(blank=True, null=True)
    pre_response_date = models.DateField(blank=True, null=True)
    response_date = models.DateField(blank=True, null=True)
    first_session_date = models.DateField(blank=True, null=True)
    first_session_response_date = models.DateField(blank=True, null=True)
    first_session_response_date_plus_30_days = models.DateField(blank=True, null=True)
    response_rada = models.CharField(default='', max_length=30, choices=RESPONSE_RADA_CHOISE, blank=True, null=True)
    oskargenya_1 = models.CharField(default='', max_length=40, blank=True, null=True)
    dev_message_mov_zgoda = models.CharField(default='', max_length=40, blank=True, null=True)
    oskargenya_2 = models.CharField(default='', max_length=40, blank=True, null=True)
    sending_date_zatverg = models.DateField(blank=True, null=True)
    sending_response_date_zatverg = models.DateField(blank=True, null=True)
    sending_response_date_zatverg_plus_14_days = models.DateField(blank=True, null=True)
    oskargenya_zatverg = models.CharField(default='', max_length=40, blank=True, null=True)
    register = models.CharField(default='', max_length=40, blank=True, null=True)
    #dev
    vidpovidalny = models.ForeignKey(Vipovilny, on_delete=models.CASCADE, blank=True, null=True)
    first_date = models.DateField(blank=True, null=True)
    akt_vigotovleno_date = models.DateField(blank=True, null=True)
    akt_pidpisano_date = models.DateField(blank=True, null=True)
    granichniy_complete_date = models.DateField(blank=True, null=True)
    complite_date = models.DateField(blank=True, null=True)
    pogodjenya = models.CharField(max_length=50, default='', blank=True, null=True)
    expertise = models.CharField(max_length=50, default='', blank=True, null=True)
    podonya_date = models.DateField(blank=True, null=True)
    number_ZV = models.CharField(max_length=50, default='', blank=True, null=True)
    register_ZD = models.CharField(max_length=50, default='', blank=True, null=True)
    #buchalter
    total = models.CharField(max_length=50, default='', blank=True, null=True)
    payed = models.CharField(max_length=50, default='', blank=True, null=True)
    #note
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.order_number

