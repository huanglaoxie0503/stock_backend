from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'

    def ready(self):
        from apps.users import signals  # 确保在应用程序加载后导入信号或其他初始化代码
