# Generated by Django 3.1 on 2020-09-02 13:49

from django.db import migrations, models
import papers.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=1000)),
                ('status', models.CharField(default='pending', max_length=255)),
                ('comment', models.CharField(max_length=255, null=True)),
                ('keyword', models.CharField(max_length=255)),
                ('file', models.FileField(null=True, upload_to=papers.models.media_location)),
                ('is_poster', models.BooleanField(default=False)),
            ],
        ),
    ]
