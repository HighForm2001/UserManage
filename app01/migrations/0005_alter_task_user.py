# Generated by Django 4.1.7 on 2023-03-03 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_alter_task_detail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='user',
            field=models.CharField(max_length=64, verbose_name='负责人'),
        ),
    ]