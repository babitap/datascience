# Generated by Django 2.1.11 on 2020-04-26 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access_control', '0003_auto_20200311_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='entities',
            field=models.ManyToManyField(blank=True, help_text='The entities this user belongs to.', related_name='user_set', related_query_name='user', to='access_control.Entity', verbose_name='entities'),
        ),
    ]
