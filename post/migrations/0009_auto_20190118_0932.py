# Generated by Django 2.1.5 on 2019-01-18 07:32

from django.db import migrations
import post.models
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0008_remove_comment_moderation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='logo',
            field=stdimage.models.StdImageField(default='', upload_to=post.models.upload_location),
        ),
    ]
