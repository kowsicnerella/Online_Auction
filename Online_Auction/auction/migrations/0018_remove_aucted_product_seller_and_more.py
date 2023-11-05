# Generated by Django 4.2.6 on 2023-11-04 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0017_aucted_product_win_ner_alter_aucted_product_winner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aucted_product',
            name='seller',
        ),
        migrations.RemoveField(
            model_name='aucted_product',
            name='win_ner',
        ),
        migrations.AddField(
            model_name='aucted_product',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auction.auction_user'),
        ),
    ]