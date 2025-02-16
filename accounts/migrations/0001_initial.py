# Generated by Django 5.0.6 on 2024-07-07 06:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='accounts/images/')),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('phone_no', models.CharField(blank=True, max_length=12, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Male', max_length=10, null=True)),
                ('city', models.CharField(blank=True, max_length=30, null=True)),
                ('relationship', models.CharField(blank=True, choices=[('Single', 'Single'), ('In a relationship', 'In a relationship'), ('Engaged', 'Engaged'), ('Married', 'Married')], default='Single', max_length=30, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
