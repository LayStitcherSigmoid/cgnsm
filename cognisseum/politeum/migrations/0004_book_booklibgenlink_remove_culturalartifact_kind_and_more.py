# Generated by Django 5.0.7 on 2024-09-19 16:36

import django.db.models.deletion
import politeum.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrarium', '0003_ontologicalrelationtype_ontologion_and_more'),
        ('politeum', '0003_alternativecountryname_culturalartifactmetalink_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('title', models.CharField(max_length=100)),
                ('edition', models.CharField(blank=True, max_length=20, null=True)),
                ('isbn', models.CharField(max_length=100)),
            ],
            bases=('administrarium.pragmon',),
        ),
        migrations.CreateModel(
            name='BookLibGenLink',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('link', models.URLField()),
            ],
            bases=('administrarium.pragmon',),
        ),
        # migrations.RemoveField(
        #     model_name='culturalartifact',
        #     name='kind',
        # ),
        # migrations.RemoveField(
        #     model_name='culturalartifact',
        #     name='pragmon_ptr',
        # ),
        # migrations.RemoveField(
        #     model_name='culturalartifactmeta',
        #     name='cultural_artifact',
        # ),
        # migrations.RemoveField(
        #     model_name='culturalartifactontology',
        #     name='artifact',
        # ),
        # migrations.RemoveField(
        #     model_name='culturalartifactmeta',
        #     name='meta',
        # ),
        # migrations.RemoveField(
        #     model_name='culturalartifactmeta',
        #     name='pragmon_ptr',
        # ),
        # migrations.RemoveField(
        #     model_name='culturalartifactmetalink',
        #     name='field',
        # ),
        # migrations.RemoveField(
        #     model_name='culturalartifactmetalink',
        #     name='kind',
        # ),
        # migrations.RemoveField(
        #     model_name='culturalartifactmetalink',
        #     name='pragmon_ptr',
        # ),
        # migrations.RemoveField(
        #     model_name='culturalartifactontology',
        #     name='pragmon_ptr',
        # ),
        # migrations.RemoveField(
        #     model_name='culturalartifactontology',
        #     name='relevant_ontologion',
        # ),
        # migrations.RemoveField(
        #     model_name='culturalartifacttype',
        #     name='pragmon_ptr',
        # ),
        # migrations.RemoveField(
        #     model_name='culturalartifacttypemetafield',
        #     name='pragmon_ptr',
        # ),
        migrations.AddField(
            model_name='person',
            name='middle_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='person',
            name='mononym',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='person',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='death_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Authorship',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('date', models.DateField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='politeum.person')),
                ('relevant_book', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='politeum.book')),
            ],
            bases=('administrarium.pragmon',),
        ),
        migrations.CreateModel(
            name='BookFile',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('path', models.FileField(upload_to=politeum.models.user_directory_path)),
                ('relevant_book', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='politeum.book')),
            ],
            bases=('administrarium.pragmon',),
        ),
        migrations.CreateModel(
            name='LibGenLinkToFile',
            fields=[
                ('pragmon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administrarium.pragmon')),
                ('relevant_file', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='politeum.bookfile')),
                ('relevant_link', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='politeum.booklibgenlink')),
            ],
            bases=('administrarium.pragmon',),
        ),
        migrations.DeleteModel(
            name='AlternativeCountryName',
        ),
        migrations.DeleteModel(
            name='CulturalArtifact',
        ),
        migrations.DeleteModel(
            name='CulturalArtifactMeta',
        ),
        migrations.DeleteModel(
            name='CulturalArtifactMetaLink',
        ),
        migrations.DeleteModel(
            name='CulturalArtifactOntology',
        ),
        migrations.DeleteModel(
            name='CulturalArtifactType',
        ),
        migrations.DeleteModel(
            name='CulturalArtifactTypeMetaField',
        ),
    ]
