# Generated by Django 4.0.4 on 2022-04-12 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver_Standing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season', models.IntegerField()),
                ('round', models.IntegerField()),
                ('position', models.IntegerField()),
                ('driver_id', models.CharField(max_length=100)),
                ('team_id', models.CharField(max_length=100)),
                ('points', models.FloatField()),
                ('wins', models.IntegerField()),
            ],
        ),
    ]
