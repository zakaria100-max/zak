# Generated by Django 3.0.4 on 2020-03-13 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0002_author_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='benutzer',
            name='jahr',
            field=models.IntegerField(default=23),
            preserve_default=False,
        ),
    ]
