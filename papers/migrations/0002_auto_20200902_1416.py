# Generated by Django 3.1 on 2020-09-02 14:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('papers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='approved_paper',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='paper', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paper',
            name='approved_poster',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='poster', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paper',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to=settings.AUTH_USER_MODEL),
        ),
    ]
