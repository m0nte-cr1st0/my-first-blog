# Generated by Django 2.1.5 on 2019-01-18 21:10

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_auto_20190118_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
