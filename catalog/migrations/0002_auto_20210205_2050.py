# Generated by Django 3.1.6 on 2021-02-05 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='date_of_deate',
            new_name='date_of_death',
        ),
    ]
