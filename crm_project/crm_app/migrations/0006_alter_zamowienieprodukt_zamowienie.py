# Generated by Django 5.0.1 on 2024-10-08 00:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0005_remove_zamowienie_produkty_zamowienieprodukt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zamowienieprodukt',
            name='zamowienie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zamowienie_produkty', to='crm_app.zamowienie'),
        ),
    ]
