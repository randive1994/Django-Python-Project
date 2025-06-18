from django.apps import AppConfig


class ShopAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop_app'
     
    def ready(self):
        from .task import start_worker_pool, setup_signal_handlers
        start_worker_pool(num_workers=3)
        setup_signal_handlers()