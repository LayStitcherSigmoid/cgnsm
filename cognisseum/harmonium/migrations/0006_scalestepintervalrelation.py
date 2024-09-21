# Generated by Django 5.0.7 on 2024-09-16 20:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrarium', '0003_ontologicalrelationtype_ontologion_and_more'),
        ('harmonium', '0005_remove_equave_ratio_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScaleStepIntervalRelation',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('first_interval', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='source_interval', to='harmonium.interval')),
                ('relative_step', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='harmonium.scalestep')),
                ('second_interval', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='target_interval', to='harmonium.interval')),
            ],
            bases=('administrarium.pragmon',),
        ),
    ]
