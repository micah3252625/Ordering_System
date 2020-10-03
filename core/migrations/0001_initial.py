# Generated by Django 3.1.1 on 2020-10-02 07:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True)),
                ('price', models.FloatField()),
                ('category', models.CharField(choices=[('Pizzalet', 'Pizzalet'), ('Pizza', 'Pizza')], default='Pizza', max_length=10)),
                ('label', models.CharField(choices=[('primary', 'primary'), ('secondary', 'secondary'), ('danger', 'danger')], default='primary', max_length=10)),
                ('size', models.IntegerField(choices=[(8, 8), (10, 10), (12, 12)], default=8, null=True)),
                ('slug', models.SlugField()),
                ('image', models.ImageField(null=True, upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='OrderPizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('is_ordered', models.BooleanField(default=False)),
                ('pizza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.pizza')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('contact', models.CharField(max_length=11)),
                ('street', models.CharField(max_length=100)),
                ('barangay', models.CharField(max_length=100)),
                ('text', models.TextField(blank=True, max_length=250, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('ordered_date', models.DateTimeField()),
                ('is_ordered', models.BooleanField(default=False)),
                ('pizzas', models.ManyToManyField(to='core.OrderPizza')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
