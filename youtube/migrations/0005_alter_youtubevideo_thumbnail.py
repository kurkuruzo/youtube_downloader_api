# Generated by Django 4.1.2 on 2022-10-09 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youtube', '0004_alter_youtubevideo_options_alter_youtubevideo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youtubevideo',
            name='thumbnail',
            field=models.URLField(blank=True, null=True),
        ),
    ]
