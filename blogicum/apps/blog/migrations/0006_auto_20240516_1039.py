# Generated by Django 3.2.16 on 2024-05-16 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20240516_1016'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-pub_date',), 'verbose_name': 'публикация', 'verbose_name_plural': 'Публикации'},
        ),
        migrations.AlterModelManagers(
            name='post',
            managers=[
            ],
        ),
    ]