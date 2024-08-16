# Generated by Django 5.0.7 on 2024-08-14 20:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administrarium', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccidentalSystem',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('name', models.CharField(max_length=50)),
            ],
            bases=('administrarium.pragmon',),
        ),
        migrations.CreateModel(
            name='Clef',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('name', models.CharField(max_length=20)),
            ],
            bases=('administrarium.pragmon',),
        ),
        migrations.CreateModel(
            name='Enharmonic',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('chromatic_number', models.IntegerField()),
            ],
            bases=('administrarium.pragmon',),
        ),
        migrations.CreateModel(
            name='Equave',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('name', models.CharField(max_length=20)),
                ('ratio', models.IntegerField()),
            ],
            bases=('administrarium.pragmon',),
        ),
        migrations.CreateModel(
            name='Interval',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('step_mod', models.IntegerField(blank=True)),
                ('numerator_mod', models.IntegerField(blank=True)),
                ('denominator_mod', models.IntegerField(blank=True)),
                ('name', models.CharField(max_length=10)),
            ],
            bases=('administrarium.pragmon',),
        ),
        migrations.CreateModel(
            name='IntervalQuality',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('name', models.CharField(max_length=20)),
            ],
            bases=('administrarium.pragmon',),
        ),
        migrations.CreateModel(
            name='NoteName',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('name', models.CharField(max_length=20)),
            ],
            bases=('administrarium.pragmon',),
        ),
        migrations.CreateModel(
            name='Temperament',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('name', models.CharField(max_length=20)),
                ('has_step_basis', models.BooleanField()),
                ('has_ratio_basis', models.BooleanField()),
            ],
            bases=('administrarium.pragmon',),
        ),
        migrations.CreateModel(
            name='EnharmonicClefPosition',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('position', models.IntegerField()),
                ('relative_clef', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='harmonium.clef')),
                ('relative_enharmonic', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='harmonium.enharmonic')),
            ],
            bases=('administrarium.pragmon',),
        ),
        migrations.CreateModel(
            name='Accidental',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('name', models.CharField(max_length=20)),
                ('symbol', models.CharField(max_length=5)),
                ('accidental_system', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='harmonium.accidentalsystem')),
                ('interval_mod', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='harmonium.interval')),
            ],
            bases=('administrarium.pragmon',),
        ),
        migrations.AddField(
            model_name='interval',
            name='quality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='harmonium.intervalquality'),
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('relative_accidental', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='harmonium.accidental')),
                ('note_name', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='harmonium.notename')),
            ],
            bases=('administrarium.pragmon',),
        ),
        migrations.CreateModel(
            name='EnharmonicEquivalence',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('cell', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='harmonium.enharmonic')),
                ('element', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='harmonium.note')),
            ],
            bases=('administrarium.pragmon',),
        ),
        migrations.AddField(
            model_name='clef',
            name='bottom_note',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='harmonium.notename'),
        ),
        migrations.CreateModel(
            name='TuningSystem',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('name', models.CharField(max_length=20)),
                ('chromaticity', models.IntegerField()),
                ('relative_equave', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='harmonium.equave')),
                ('relative_temperament', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='harmonium.temperament')),
            ],
            bases=('administrarium.pragmon',),
        ),
        migrations.AddField(
            model_name='note',
            name='tuning_system',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='harmonium.tuningsystem'),
        ),
        migrations.AddField(
            model_name='enharmonic',
            name='tuning_system',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='harmonium.tuningsystem'),
        ),
    ]