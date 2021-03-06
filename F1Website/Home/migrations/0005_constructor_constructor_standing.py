# Generated by Django 4.0.4 on 2022-04-12 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0004_circuit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Constructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_id', models.CharField(max_length=100)),
                ('team_name', models.CharField(max_length=100)),
                ('nationality', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Constructor_Standing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season', models.IntegerField()),
                ('team_id', models.CharField(max_length=100)),
                ('team_name', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=100)),
                ('points', models.FloatField()),
                ('wins', models.IntegerField()),
            ],
        ),
    ]
