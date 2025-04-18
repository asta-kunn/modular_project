# Generated by Django 5.1.7 on 2025-03-08 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("engine", "0004_alter_installedmodule_installed_version_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="installedmodule",
            name="installed_version",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="module",
            name="landing_url_name",
            field=models.CharField(
                blank=True,
                help_text="Django URL name untuk landing page modul, misal 'product_module:landing'",
                max_length=100,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="module",
            name="version",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
