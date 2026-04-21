from django.contrib.admin import AdminSite
from django.urls import path
from .views import search_vehicle

class CustomAdminSite(AdminSite):
    site_header = 'Администрирование ГИБДД'
    site_title = 'ГИБДД'
    index_title = 'Учёт транспортных средств'
    index_template = 'admin/custom_index.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('search/', search_vehicle, name='search_vehicle'),
        ]
        return custom_urls + urls

custom_admin_site = CustomAdminSite(name='custom_admin')