# Generated by Django 3.1.1 on 2020-09-11 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zemradnyk', '0021_auto_20200910_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='exist_mark',
            field=models.CharField(blank=True, choices=[('✓', '✓'), ('✕', '✕')], default='✕', max_length=10, null=True),
        ),
    ]
