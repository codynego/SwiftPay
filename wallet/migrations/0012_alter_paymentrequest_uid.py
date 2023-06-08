# Generated by Django 4.1.5 on 2023-06-08 04:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0011_alter_paymentrequest_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentrequest',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True),
        ),
    ]
