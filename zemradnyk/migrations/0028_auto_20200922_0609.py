# Generated by Django 3.1.1 on 2020-09-22 06:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zemradnyk', '0027_auto_20200921_0816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='developer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='developer', to='zemradnyk.rozrobnik'),
        ),
    ]