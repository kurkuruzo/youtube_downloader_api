# Generated by Django 4.1.2 on 2022-10-09 10:35

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='YouTubeVideo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('url', models.CharField(max_length=1500)),
                ('path', models.CharField(max_length=1500)),
                ('length', models.IntegerField()),
                ('date_added', models.DateTimeField()),
            ],
        ),
    ]