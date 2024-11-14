# Generated by Django 5.1 on 2024-09-03 18:28

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebPages', '0009_faq'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jobopening',
            options={'ordering': ['-posted_date'], 'verbose_name': 'Вакансия', 'verbose_name_plural': 'Вакансии'},
        ),
        migrations.RemoveField(
            model_name='jobopening',
            name='is_active',
        ),
        migrations.AddField(
            model_name='jobopening',
            name='location',
            field=models.CharField(blank=True, max_length=200, verbose_name='Местоположение'),
        ),
        migrations.AddField(
            model_name='jobopening',
            name='posted_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата публикации'),
        ),
        migrations.AddField(
            model_name='jobopening',
            name='responsibilities',
            field=models.TextField(blank=True, verbose_name='Обязанности'),
        ),
        migrations.AlterField(
            model_name='jobopening',
            name='description',
            field=models.TextField(verbose_name='Описание вакансии'),
        ),
        migrations.AlterField(
            model_name='jobopening',
            name='requirements',
            field=models.TextField(blank=True, verbose_name='Требования'),
        ),
    ]
