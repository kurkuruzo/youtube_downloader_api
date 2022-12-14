# Generated by Django 4.1.2 on 2022-10-09 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youtube', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='youtubevideo',
            name='description',
            field=models.TextField(blank=True, max_length=3500, null=True),
        ),
        migrations.AddField(
            model_name='youtubevideo',
            name='thumbnail',
            field=models.ImageField(default='', upload_to=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='youtubevideo',
            name='path',
            field=models.CharField(blank=True, max_length=1500, null=True),
        ),
    ]
