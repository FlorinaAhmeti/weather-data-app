# Generated by Django 3.2.6 on 2024-11-06 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stations', '0001_initial'),
        ('weather_master_x', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='weathermasterx',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='weathermasterx',
            name='station_identifier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weather_master_x', to='stations.station'),
        ),
    ]