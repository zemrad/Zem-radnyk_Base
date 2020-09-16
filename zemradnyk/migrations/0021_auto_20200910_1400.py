# Generated by Django 3.1.1 on 2020-09-10 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zemradnyk', '0020_auto_20200910_0752'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vipovilny',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='vidpovidalny',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.CASCADE, to='zemradnyk.vipovilny'),
        ),
    ]
