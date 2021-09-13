# Generated by Django 3.2.6 on 2021-09-12 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='battery_status',
            field=models.CharField(default='ON', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='battery_voltage',
            field=models.CharField(default='1.25', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='energy_curr',
            field=models.CharField(default='22', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='panel_voltage',
            field=models.CharField(default='2343', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='power_panel',
            field=models.CharField(default='2343', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(default='2323', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='total_energy',
            field=models.CharField(default='2211', max_length=255),
            preserve_default=False,
        ),
    ]