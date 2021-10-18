# Generated by Django 3.2.7 on 2021-09-25 21:08

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
            name='Emission_parameters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('substance_name', models.CharField(max_length=50)),
                ('substance_type', models.CharField(max_length=50)),
                ('permissible_limit', models.IntegerField()),
                ('unit', models.CharField(max_length=20)),
                ('relation', models.CharField(default='max', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(default='viewer', max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Survey_metadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('population', models.IntegerField()),
                ('num_issues', models.IntegerField()),
                ('relevant_issues', models.IntegerField()),
                ('resolved_issues', models.IntegerField(default=0)),
                ('auditor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.person')),
            ],
        ),
        migrations.CreateModel(
            name='Survey_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person', models.CharField(max_length=50)),
                ('feedback', models.TextField()),
                ('status', models.CharField(max_length=20)),
                ('last_date', models.DateField(auto_now=True)),
                ('survey_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.survey_metadata')),
                ('surveyor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.person')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.person')),
            ],
        ),
        migrations.CreateModel(
            name='Phone_no',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_no', models.IntegerField()),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.person')),
            ],
        ),
        migrations.CreateModel(
            name='Complaints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complaint', models.TextField()),
                ('rules_violated', models.TextField()),
                ('status', models.CharField(default='Relevant', max_length=15)),
                ('last_update', models.DateField(auto_now=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.person')),
            ],
        ),
        migrations.CreateModel(
            name='Company_emissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('session', models.ManyToManyField(to='my_app.Session')),
                ('substance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.emission_parameters')),
            ],
        ),
    ]
