from django.db import models

class Owner(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="ФИО")
    passport = models.CharField(max_length=20, verbose_name="Паспорт")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    address = models.TextField(blank=True, verbose_name="Адрес")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Владелец"
        verbose_name_plural = "Владельцы"


class Vehicle(models.Model):
    vin = models.CharField(max_length=17, unique=True, verbose_name="VIN")
    license_plate = models.CharField(max_length=10, unique=True, verbose_name="Госномер")
    brand = models.CharField(max_length=50, verbose_name="Марка")
    model = models.CharField(max_length=50, verbose_name="Модель")
    year = models.IntegerField(verbose_name="Год выпуска")
    color = models.CharField(max_length=30, verbose_name="Цвет")

    def __str__(self):
        return f"{self.license_plate} ({self.brand} {self.model})"

    class Meta:
        verbose_name = "Транспортное средство"
        verbose_name_plural = "Транспортные средства"


class Registration(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, verbose_name="ТС")
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name="Владелец")
    reg_date = models.DateField(auto_now_add=True, verbose_name="Дата регистрации")
    end_date = models.DateField(null=True, blank=True, verbose_name="Дата снятия")
    is_active = models.BooleanField(default=True, verbose_name="Действует")

    def __str__(self):
        return f"{self.vehicle} - {self.owner}"

    class Meta:
        verbose_name = "Регистрация"
        verbose_name_plural = "Регистрации"


class Fine(models.Model):
    STATUS_CHOICES = [
        ('unpaid', 'Не оплачен'),
        ('paid', 'Оплачен'),
        ('appealed', 'Обжалован'),
    ]
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, verbose_name="ТС")
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name="Владелец")
    number = models.CharField(max_length=50, unique=True, verbose_name="Номер постановления")
    date = models.DateField(verbose_name="Дата нарушения")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма (руб.)")
    description = models.TextField(blank=True, verbose_name="Описание нарушения")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unpaid', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата оплаты")

    def __str__(self):
        return f"Штраф {self.number} - {self.amount} руб."

    class Meta:
        verbose_name = "Штраф"
        verbose_name_plural = "Штрафы"
        ordering = ['-date']


class Restriction(models.Model):
    RESTRICTION_TYPES = [
        ('stolen', 'Угон'),
        ('arrest', 'Арест'),
        ('ban_registration', 'Запрет регистрационных действий'),
        ('pledge', 'Залог'),
        ('wanted', 'В розыске'),
    ]
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, verbose_name="ТС")
    restriction_type = models.CharField(max_length=30, choices=RESTRICTION_TYPES, verbose_name="Тип ограничения")
    start_date = models.DateField(auto_now_add=True, verbose_name="Дата начала")
    end_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания")
    is_active = models.BooleanField(default=True, verbose_name="Действует")
    document_number = models.CharField(max_length=50, blank=True, verbose_name="Номер документа")
    initiator = models.CharField(max_length=200, blank=True, verbose_name="Инициатор (суд, пристав, полиция)")
    description = models.TextField(blank=True, verbose_name="Описание")
    
    def __str__(self):
        return f"{self.get_restriction_type_display()} на {self.vehicle} - {'Активно' if self.is_active else 'Снято'}"
    
    class Meta:
        verbose_name = "Ограничение"
        verbose_name_plural = "Ограничения"
        ordering = ['-start_date']