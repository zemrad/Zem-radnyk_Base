# Generated by Django 3.1.1 on 2020-09-17 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zemradnyk', '0025_auto_20200913_1819'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kadastr_Number',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kadastr_number', models.CharField(max_length=100)),
            ],
        ),
    ]