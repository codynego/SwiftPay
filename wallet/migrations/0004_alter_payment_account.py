# Generated by Django 4.1.5 on 2023-06-05 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0003_alter_account_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='wallet.account'),
        ),
    ]