# Generated by Django 4.1.7 on 2023-06-02 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_news', '0003_news_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='owner',
        ),
    ]