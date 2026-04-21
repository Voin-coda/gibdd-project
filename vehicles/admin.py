from django.contrib import admin
from django.contrib import messages
from .admin_site import custom_admin_site
from .models import Owner, Vehicle, Registration, Fine, Restriction

# Кастомный админ для регистраций с проверкой ограничений
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'owner', 'reg_date', 'is_active']
    list_filter = ['is_active', 'reg_date']
    search_fields = ['vehicle__license_plate', 'owner__full_name']
    
    def save_model(self, request, obj, form, change):
        # Проверяем ограничения при создании активной регистрации
        if obj.is_active:
            active_restrictions = Restriction.objects.filter(vehicle=obj.vehicle, is_active=True)
            if active_restrictions.exists():
                restriction_list = ", ".join([r.get_restriction_type_display() for r in active_restrictions])
                messages.error(request, f"❌ Невозможно зарегистрировать ТС {obj.vehicle.license_plate}! Активные ограничения: {restriction_list}")
                return
        super().save_model(request, obj, form, change)

# Кастомный админ для ограничений
class RestrictionAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'restriction_type', 'start_date', 'is_active', 'initiator']
    list_filter = ['restriction_type', 'is_active']
    search_fields = ['vehicle__license_plate', 'document_number', 'initiator']
    readonly_fields = ['start_date']  # поле только для чтения (автозаполнение)
    fieldsets = (
        ('Основная информация', {
            'fields': ('vehicle', 'restriction_type', 'is_active')
        }),
        ('Документы', {
            'fields': ('document_number', 'initiator'),
            'classes': ('wide',)
        }),
        ('Даты', {
            'fields': ('end_date',),  # start_date исключён, так как readonly
            'classes': ('wide',)
        }),
        ('Описание', {
            'fields': ('description',),
            'classes': ('wide',)
        }),
    )

# Регистрируем модели в кастомном сайте
custom_admin_site.register(Owner)
custom_admin_site.register(Vehicle)
custom_admin_site.register(Registration, RegistrationAdmin)
custom_admin_site.register(Fine)
custom_admin_site.register(Restriction, RestrictionAdmin)