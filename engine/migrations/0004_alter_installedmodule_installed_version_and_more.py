# Generated by Django 5.1.7 on 2025-03-08 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("engine", "0003_module_landing_url_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="installedmodule",
            name="installed_version",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="module",
            name="landing_url_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="module",
            name="version",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
