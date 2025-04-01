# Login Credential 

## Role Manager
username = manager
password = manager

## Role User
username = user
password = user

## Role Public
username = public
password = public

# Make a new module
```
python manage.py shell
```

then

```
from engine.models import Module
product_module, created = Module.objects.get_or_create(
    slug='product-module',
    defaults={
        'name': 'Product Module',
        'is_installed': True,
        'version': '1.0',
        'landing_url_name': 'product_module:landing'  # Pastikan URL name sesuai dengan yang didefinisikan di product_module.urls
    }
)
```