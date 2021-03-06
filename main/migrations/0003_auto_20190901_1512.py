# Generated by Django 2.2.4 on 2019-09-01 14:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20190831_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='bcardno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_booking_card', related_query_name='main_bookings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='booking',
            name='bempno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_booking_emp', related_query_name='main_bookings', to=settings.AUTH_USER_MODEL),
        ),
    ]
