from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.news'
    # fa fa-bullhorn
    # model_icon = 'fa fa-bullhorn'
    verbose_name = "新闻资讯"
    orderIndex = 4
