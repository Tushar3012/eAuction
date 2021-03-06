# Generated by Django 3.1.3 on 2021-01-15 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('catid', models.AutoField(primary_key=True, serialize=False)),
                ('catnm', models.CharField(max_length=50, unique=True)),
                ('caticonnm', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('subcatid', models.AutoField(primary_key=True, serialize=False)),
                ('catnm', models.CharField(max_length=50)),
                ('subcatnm', models.CharField(max_length=50, unique=True)),
                ('subcaticonnm', models.CharField(max_length=500)),
            ],
        ),
    ]
