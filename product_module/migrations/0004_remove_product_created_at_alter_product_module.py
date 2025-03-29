# Generated by Django 5.1.7 on 2025-03-08 15:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("engine", "0005_alter_installedmodule_installed_version_and_more"),
        ("product_module", "0003_product_created_at_alter_product_module"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="created_at",
        ),
        migrations.AlterField(
            model_name="product",
            name="module",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="products",
                to="engine.module",
            ),
        ),
    ]
