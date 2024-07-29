# -*- coding: utf-8 -*-
from collections import OrderedDict

from django.core.paginator import Paginator as DjangoPaginator
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.core.paginator import InvalidPage


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 999
    django_paginator_class = DjangoPaginator

    def __init__(self):
        super().__init__()
        self.request = None
        self.page = None

    def paginate_queryset(self, queryset, request, view=None):
        """
        重写 paginate_queryset 方法，使分页超过正常分页时返回自定义响应。
        原来超过分页返回 400 错误，改为返回 200 状态码和空数据。
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        custom_paginator = self.django_paginator_class(queryset, page_size)
        page_number = self.get_page_number(request, custom_paginator)

        try:
            self.page = custom_paginator.page(page_number)
        except InvalidPage:
            self.page = []

        if custom_paginator.num_pages > 1 and self.template is not None:
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):
        """
        重写 get_paginated_response 方法，自定义分页响应格式。
        """
        # 获取当前页码
        current_page = int(self.get_page_number(self.request, self.page.paginator)) if self.page else 1
        # 获取每页大小
        limit = int(self.get_page_size(self.request)) or 10
        # 获取总数据量
        total = self.page.paginator.count if self.page else 0

        # 构建响应数据
        res = {
            'page': current_page,
            'total': total,
            'limit': limit,
            'data': data
        }
        # 如果没有数据，设置提示信息
        if not data:
            res['data'] = []
            msg = '暂无数据'
        else:
            msg = 'success'

        return Response(OrderedDict([
            ('code', 2000),
            ('msg', msg),
            ('data', res),
        ]))
