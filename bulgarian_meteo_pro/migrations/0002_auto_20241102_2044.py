# Generated by Django 3.2.6 on 2024-11-02 20:44

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('stations', '0001_initial'),
        ('bulgarian_meteo_pro', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bulgarianmeteoprodata',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bulgarianmeteoprodata',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='bulgarianmeteoprodata',
            name='station_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='stations.station'),
        ),
    ]
