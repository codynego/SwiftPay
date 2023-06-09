# Generated by Django 4.1.5 on 2023-06-09 09:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentLInk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('link', models.URLField(blank=True, max_length=50, null=True)),
                ('qrcode', models.ImageField(blank=True, null=True, upload_to='img')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='paymentlinks',
            name='basepayment_ptr',
        ),
        migrations.RemoveField(
            model_name='paymentqrcode',
            name='basepayment_ptr',
        ),
        migrations.DeleteModel(
            name='BasePayment',
        ),
        migrations.DeleteModel(
            name='paymentlinks',
        ),
        migrations.DeleteModel(
            name='PaymentQrcode',
        ),
    ]
