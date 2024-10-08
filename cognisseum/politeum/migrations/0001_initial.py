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
            name='Country',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('name', models.CharField(max_length=200)),
            ],
            bases=('administrarium.pragmon',),
        ),
        migrations.CreateModel(
            name='CulturalArtifact',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('title', models.CharField(max_length=100)),
                ('subtitle', models.CharField(blank=True, max_length=100)),
            ],
            bases=('administrarium.pragmon',),
        ),
        migrations.CreateModel(
            name='CulturalArtifactMetaType',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('field_name', models.CharField(max_length=100)),
            ],
            bases=('administrarium.pragmon',),
        ),
        migrations.CreateModel(
            name='CulturalArtifactType',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('name', models.CharField(max_length=100)),
            ],
            bases=('administrarium.pragmon',),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('birth_date', models.DateField()),
                ('death_date', models.DateField()),
            ],
            bases=('administrarium.pragmon',),
        ),
        migrations.CreateModel(
            name='CulturalArtifactMeta',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('cultural_artifact', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='politeum.culturalartifact')),
                ('meta', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='politeum.culturalartifactmetatype')),
            ],
            bases=('administrarium.pragmon',),
        ),
        migrations.CreateModel(
            name='CulturalArtifactReview',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('review', models.TextField()),
                ('decimal_rating', models.IntegerField()),
                ('artifact', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='politeum.culturalartifact')),
            ],
            bases=('administrarium.pragmon',),
        ),
        migrations.AddField(
            model_name='culturalartifactmetatype',
            name='meta_kind',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='politeum.culturalartifacttype'),
        ),
        migrations.AddField(
            model_name='culturalartifact',
            name='kind',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='politeum.culturalartifacttype'),
        ),
        migrations.CreateModel(
            name='FirstLevelDivision',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('name', models.CharField(max_length=200)),
                ('relative_country', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='politeum.country')),
            ],
            bases=('administrarium.pragmon',),
        ),
        migrations.CreateModel(
            name='Biography',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('bio', models.TextField()),
                ('relative_person', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='politeum.person')),
            ],
            bases=('administrarium.pragmon',),
        ),
        migrations.CreateModel(
            name='SecondLevelDivision',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('name', models.CharField(max_length=200)),
                ('first_div', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='politeum.firstleveldivision')),
            ],
            bases=('administrarium.pragmon',),
        ),
    ]
