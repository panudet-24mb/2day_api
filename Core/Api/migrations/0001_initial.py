# Generated by Django 3.0.3 on 2020-11-07 18:04

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('company_id', models.AutoField(primary_key=True, serialize=False)),
                ('company_public_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('company_name', models.CharField(blank=True, max_length=180, null=True, unique=True)),
                ('company_is_active', models.BooleanField(default=False)),
                ('created_on', models.DateField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'company',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('department_id', models.AutoField(primary_key=True, serialize=False)),
                ('department_name', models.CharField(blank=True, max_length=80, null=True)),
            ],
            options={
                'db_table': 'department',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('position_id', models.AutoField(primary_key=True, serialize=False)),
                ('position_name', models.CharField(blank=True, max_length=80, null=True)),
            ],
            options={
                'db_table': 'position',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('status_id', models.AutoField(primary_key=True, serialize=False)),
                ('status_name', models.CharField(blank=True, max_length=80, null=True)),
            ],
            options={
                'db_table': 'status',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('users_id', models.AutoField(primary_key=True, serialize=False)),
                ('users_uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('users_citizen_id', models.CharField(max_length=14, unique=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Userdetails',
            fields=[
                ('userdetails_id', models.AutoField(primary_key=True, serialize=False)),
                ('userdetails_firstname', models.CharField(blank=True, max_length=80, null=True)),
                ('userdetails_lastname', models.CharField(blank=True, max_length=80, null=True)),
                ('userdetails_phone', models.CharField(blank=True, max_length=80, null=True)),
                ('userdetails_email', models.CharField(blank=True, max_length=80, null=True)),
                ('userdetails_avatar', models.CharField(blank=True, max_length=104, null=True)),
                ('userdetails_department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Api.Department')),
                ('userdetails_position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Api.Position')),
                ('users', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Api.Users')),
            ],
            options={
                'db_table': 'userdetails',
            },
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('token_id', models.AutoField(primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=255, unique=True)),
                ('token_created', models.DateTimeField()),
                ('token_active', models.BooleanField(default=True)),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Api.Users')),
            ],
            options={
                'db_table': 'token',
            },
        ),
        migrations.CreateModel(
            name='Company_has_users',
            fields=[
                ('comapny_has_users_id', models.AutoField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Api.Company')),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Api.Users')),
            ],
            options={
                'db_table': 'company_has_users',
            },
        ),
    ]
