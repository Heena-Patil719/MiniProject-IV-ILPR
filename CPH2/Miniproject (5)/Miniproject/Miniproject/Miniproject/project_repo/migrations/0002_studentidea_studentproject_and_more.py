# Generated by Django 5.1.7 on 2025-04-22 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_repo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentIdea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idea', models.CharField(blank=True, max_length=255, null=True)),
                ('prototype', models.CharField(blank=True, max_length=255, null=True)),
                ('startup', models.CharField(blank=True, max_length=255, null=True)),
                ('branch', models.CharField(max_length=100)),
                ('team_leader', models.CharField(max_length=255)),
                ('mentor', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='StudentProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=255)),
                ('project_id', models.CharField(max_length=50, unique=True)),
                ('branch', models.CharField(max_length=100)),
                ('team_leader', models.CharField(max_length=255)),
                ('mentor', models.CharField(max_length=255)),
            ],
        ),
        migrations.RenameField(
            model_name='startupteammember',
            old_name='innovation_type',
            new_name='team_leader_name',
        ),
        migrations.RemoveField(
            model_name='startup',
            name='user',
        ),
        migrations.RemoveField(
            model_name='startupteammember',
            name='difference',
        ),
        migrations.RemoveField(
            model_name='startupteammember',
            name='domain',
        ),
        migrations.RemoveField(
            model_name='startupteammember',
            name='features',
        ),
        migrations.RemoveField(
            model_name='startupteammember',
            name='problem',
        ),
        migrations.RemoveField(
            model_name='startupteammember',
            name='prototype_files',
        ),
        migrations.RemoveField(
            model_name='startupteammember',
            name='solution',
        ),
        migrations.RemoveField(
            model_name='startupteammember',
            name='status_level',
        ),
        migrations.RemoveField(
            model_name='startupteammember',
            name='team_count',
        ),
        migrations.RemoveField(
            model_name='startupteammember',
            name='team_size',
        ),
        migrations.RemoveField(
            model_name='startupteammember',
            name='upload',
        ),
        migrations.RemoveField(
            model_name='startupteammember',
            name='video_url',
        ),
        migrations.AddField(
            model_name='startup',
            name='branch',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='startup',
            name='status_level',
            field=models.IntegerField(choices=[(1, 'Level 1'), (2, 'Level 2'), (3, 'Level 3')], default=1),
        ),
        migrations.AddField(
            model_name='startup',
            name='team_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='startup',
            name='innovation_development',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='startup',
            name='innovation_image',
            field=models.FileField(default='default_image.pdf', upload_to='innovation_images/'),
        ),
        migrations.AlterField(
            model_name='startup',
            name='innovation_type',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='startup',
            name='key_innovation',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='startup',
            name='registration',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='startup',
            name='sector',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='startup',
            name='team_leader_id_card',
            field=models.FileField(blank=True, null=True, upload_to='id_cards/'),
        ),
        migrations.AlterField(
            model_name='startupteammember',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
