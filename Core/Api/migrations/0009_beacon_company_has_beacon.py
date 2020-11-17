# Generated by Django 3.0.3 on 2020-11-17 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0008_announcement'),
    ]

    operations = [
        migrations.CreateModel(
            name='Beacon',
            fields=[
                ('beacon_id', models.AutoField(primary_key=True, serialize=False)),
                ('beacon_name', models.CharField(blank=True, max_length=180, null=True)),
                ('beacon_unique_uuid', models.CharField(blank=True, max_length=250, null=True)),
                ('beacon_service_uuid', models.CharField(blank=True, max_length=250, null=True)),
                ('beacon_characteristic_uuid', models.CharField(blank=True, max_length=250, null=True)),
                ('beacon_model', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('delete_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'beacon',
            },
        ),
        migrations.CreateModel(
            name='Company_has_beacon',
            fields=[
                ('comapany_has_beacon_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=False)),
                ('delete_at', models.DateTimeField(blank=True, null=True)),
                ('beacon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Api.Beacon')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Api.Company')),
            ],
            options={
                'db_table': 'company_has_beacon',
            },
        ),
    ]