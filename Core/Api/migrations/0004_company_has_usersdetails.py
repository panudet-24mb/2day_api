# Generated by Django 3.0.3 on 2020-11-08 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0003_auto_20201108_1623'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company_has_usersdetails',
            fields=[
                ('company_has_users_details_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Api.Company')),
                ('userdetails', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Api.Userdetails')),
            ],
            options={
                'db_table': 'company_has_usersdetails',
            },
        ),
    ]
