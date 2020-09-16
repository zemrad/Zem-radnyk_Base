# Generated by Django 3.1 on 2020-08-17 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zemradnyk', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='rayon',
            field=models.CharField(choices=[('loz', 'Лозовской'), ('kup', 'Купянский')], max_length=30),
        ),
        migrations.CreateModel(
            name='Geodeziya',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('start', 'Получено'), ('process', 'В процессе'), ('finish', 'Выполнена')], max_length=30)),
                ('order_number', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='zemradnyk.order')),
            ],
        ),
    ]
