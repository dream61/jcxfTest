# Generated by Django 4.1.7 on 2024-10-15 06:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledTask',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='任务名称')),
                ('cron_expression', models.CharField(max_length=100, verbose_name='CRON 表达式')),
                ('email', models.EmailField(max_length=254, verbose_name='通知邮箱')),
                ('status', models.CharField(choices=[('completed', '完成'), ('pendding', '待运行'), ('failed', '失败'), ('running', '运行中'), ('stopping', '停止')], max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
            ],
            options={
                'verbose_name': '定时任务表',
                'verbose_name_plural': '定时任务表',
            },
        ),
    ]
