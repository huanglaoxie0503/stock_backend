from django.apps import AppConfig


class StockPickerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.stock_picker'
    verbose_name = '选股器'
    orderIndex = 3
