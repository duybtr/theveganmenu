# Generated by Django 4.2.7 on 2025-03-03 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theveganmenu', '0005_alter_menuitem_additional_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='additional_info',
            field=models.CharField(blank=True, default='', max_length=5000),
        ),
    ]
