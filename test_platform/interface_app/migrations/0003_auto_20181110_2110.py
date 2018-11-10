# Generated by Django 2.0.6 on 2018-11-10 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface_app', '0002_auto_20181110_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcase',
            name='name',
            field=models.CharField(default=False, max_length=100, verbose_name='用例名称'),
        ),
        migrations.AlterField(
            model_name='testcase',
            name='par_type',
            field=models.TextField(default=False, verbose_name='参数类型'),
        ),
        migrations.AlterField(
            model_name='testcase',
            name='req_headers',
            field=models.TextField(default=False, verbose_name='header'),
        ),
        migrations.AlterField(
            model_name='testcase',
            name='req_method',
            field=models.TextField(default=False, verbose_name='请求方法'),
        ),
        migrations.AlterField(
            model_name='testcase',
            name='req_parameter',
            field=models.TextField(default=False, verbose_name='参数'),
        ),
        migrations.AlterField(
            model_name='testcase',
            name='url',
            field=models.TextField(default=False, verbose_name='请求url'),
        ),
    ]
