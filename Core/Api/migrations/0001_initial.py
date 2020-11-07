# Generated by Django 3.0.3 on 2020-11-07 17:08

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
            name='Token',
            fields=[
                ('token_id', models.AutoField(primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=255, unique=True)),
                ('token_created', models.DateTimeField()),
                ('token_active', models.DateTimeField()),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Api.Users')),
            ],
            options={
                'db_table': 'token',
            },
        ),
    ]
