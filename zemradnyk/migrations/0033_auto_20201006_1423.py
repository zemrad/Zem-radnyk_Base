# Generated by Django 3.1.1 on 2020-10-06 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zemradnyk', '0032_auto_20201006_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kadastr_number',
            name='in_work',
            field=models.CharField(choices=[('✓', '✓'), ('✕', '✕')], default='✕', max_length=10),
        ),
    ]