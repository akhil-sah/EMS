# Generated by Django 3.2.7 on 2021-10-24 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0004_alter_survey_data_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaints',
            name='feedback',
            field=models.TextField(default='None'),
        ),
    ]
