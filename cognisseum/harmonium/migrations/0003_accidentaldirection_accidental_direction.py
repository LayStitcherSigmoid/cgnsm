# Generated by Django 5.0.7 on 2024-08-16 18:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrarium', '0002_alter_pragmon_id'),
        ('harmonium', '0002_interval_symbol_intervalquality_symbol'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccidentalDirection',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('name', models.CharField(max_length=20)),
            ],
            bases=('administrarium.pragmon',),
        ),
        migrations.AddField(
            model_name='accidental',
            name='direction',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.RESTRICT, to='harmonium.accidentaldirection'),
            preserve_default=False,
        ),
    ]