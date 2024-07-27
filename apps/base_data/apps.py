from django.apps import AppConfig


class BaseDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.base_data'
    verbose_name = "基础数据"
