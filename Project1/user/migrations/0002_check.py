# Generated by Django 3.1.3 on 2021-02-02 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='check',
            fields=[
                ('cid', models.AutoField(primary_key=True, serialize=False)),
                ('uname', models.CharField(max_length=100)),
            ],
        ),
    ]
