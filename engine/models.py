from django.db import models
from django.conf import settings

class Module(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    # Global version, misalnya disimpan sebagai string timestamp user-friendly
    version = models.CharField(max_length=50, blank=True, null=True)
    is_installed = models.BooleanField(default=False)
    # Nama URL landing page, misalnya "product_module:landing"
    landing_url_name = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="Django URL name untuk landing page modul (contoh: 'product_module:landing')"
    )

    def __str__(self):
        return self.name

class InstalledModule(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    # Versi modul yang di‑install oleh user
    installed_version = models.CharField(max_length=50, blank=True, null=True)
    installed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'module')

    def __str__(self):
        return f"{self.user.username} - {self.module.name} (v: {self.installed_version})"
