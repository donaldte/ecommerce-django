# Generated by Django 4.0.3 on 2022-04-08 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produits', '0006_commande_attente'),
    ]

    operations = [
        migrations.AddField(
            model_name='commande',
            name='annuler',
            field=models.BooleanField(default=False, verbose_name='Annuler'),
        ),
        migrations.AddField(
            model_name='commande',
            name='regler',
            field=models.BooleanField(default=False, verbose_name='Regler'),
        ),
        migrations.AlterField(
            model_name='commande',
            name='attente',
            field=models.BooleanField(default=False, verbose_name='En attente'),
        ),
    ]