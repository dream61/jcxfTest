# Generated by Django 4.1.7 on 2024-10-15 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('testresult', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestReport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('report_file', models.FileField(upload_to='reports/')),
                ('generated_at', models.DateTimeField(auto_now_add=True)),
                ('test_result', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='testresult.testresult')),
            ],
            options={
                'verbose_name': '测试报告表',
                'verbose_name_plural': '测试报告表',
            },
        ),
    ]
