# Generated by Django 5.1.1 on 2024-10-16 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_noticias', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticia',
            name='publicada_em',
            field=models.DateTimeField(editable=False, help_text='dd/mm/yyyy hh:MM', null=True, verbose_name='Publicada em'),
        ),
    ]