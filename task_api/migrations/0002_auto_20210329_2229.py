# Generated by Django 3.1.7 on 2021-03-29 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personaldata',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]