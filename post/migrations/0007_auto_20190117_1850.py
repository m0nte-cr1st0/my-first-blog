# Generated by Django 2.1.5 on 2019-01-17 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_auto_20190117_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='moderation',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='moderation',
            field=models.BooleanField(default=False),
        ),
    ]