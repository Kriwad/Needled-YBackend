# Generated by Django 5.1.6 on 2025-05-28 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_postslist_content_alter_postslist_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postslist',
            name='content',
            field=models.CharField(blank=True, default=' ', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='postslist',
            name='title',
            field=models.CharField(blank=True, default='', max_length=30),
            preserve_default=False,
        ),
    ]
