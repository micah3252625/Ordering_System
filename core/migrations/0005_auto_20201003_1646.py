# Generated by Django 3.1.1 on 2020-10-03 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20201002_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderpizza',
            name='pizza',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.pizza'),
        ),
    ]
