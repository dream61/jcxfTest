# Generated by Django 4.1.7 on 2024-09-21 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('status', models.BooleanField(default=True)),
                ('is_logged_in', models.BooleanField(default=False)),
                ('project', models.CharField(blank=True, max_length=255, null=True)),
                ('module', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': '用户信息表',
                'verbose_name_plural': '用户信息表',
            },
        ),
    ]
