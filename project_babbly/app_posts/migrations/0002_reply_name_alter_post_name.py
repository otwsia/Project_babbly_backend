# Generated by Django 4.1.3 on 2022-11-12 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='name',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='name',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
