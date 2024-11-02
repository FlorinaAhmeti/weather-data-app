# Generated by Django 3.2.6 on 2024-11-02 20:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('station_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('city', models.CharField(max_length=100)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=10)),
                ('api_key', models.UUIDField(default=uuid.uuid4, editable=False, null=True, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
