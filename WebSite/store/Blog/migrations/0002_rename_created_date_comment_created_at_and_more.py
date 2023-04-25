# Generated by Django 4.1.7 on 2023-04-16 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='created_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='author',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='post',
        ),
        migrations.AddField(
            model_name='comment',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]