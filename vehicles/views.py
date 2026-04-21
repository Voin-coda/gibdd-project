from django.shortcuts import render
from .models import Vehicle, Registration, Owner, Fine, Restriction
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
import calendar

def search_vehicle(request):
    vehicle = None
    registration = None
    error = None
    restrictions = None
    
    if request.method == 'POST':
        license_plate = request.POST.get('license_plate', '').strip()
        if license_plate:
            try:
                vehicle = Vehicle.objects.get(license_plate=license_plate)
                registration = Registration.objects.filter(vehicle=vehicle, is_active=True).first()
                restrictions = Restriction.objects.filter(vehicle=vehicle, is_active=True)
            except Vehicle.DoesNotExist:
                error = f"Машина с номером {license_plate} не найдена"
        else:
            error = "Введите госномер"
    
    return render(request, 'vehicles/search.html', {
        'vehicle': vehicle,
        'registration': registration,
        'error': error,
        'restrictions': restrictions,
    })

def reports(request):
    # Общая статистика
    total_vehicles = Vehicle.objects.count()
    total_owners = Owner.objects.count()
    active_registrations = Registration.objects.filter(is_active=True).count()
    
    # Статистика по штрафам
    total_fines = Fine.objects.count()
    total_fines_amount = Fine.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    unpaid_fines = Fine.objects.filter(status='unpaid').count()
    unpaid_fines_amount = Fine.objects.filter(status='unpaid').aggregate(Sum('amount'))['amount__sum'] or 0
    paid_fines = Fine.objects.filter(status='paid').count()
    paid_fines_amount = Fine.objects.filter(status='paid').aggregate(Sum('amount'))['amount__sum'] or 0
    appealed_fines = Fine.objects.filter(status='appealed').count()
    appealed_fines_amount = Fine.objects.filter(status='appealed').aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Топ-5 машин с наибольшим количеством штрафов
    top_vehicles = Vehicle.objects.annotate(
        fines_count=Count('fine')
    ).order_by('-fines_count')[:5]
    
    # Статистика по месяцам (последние 6 месяцев)
    monthly_data = []
    today = timezone.now().date()
    
    for i in range(5, -1, -1):
        month_date = today.replace(day=1) - timedelta(days=30 * i)
        month_start = month_date.replace(day=1)
        
        if i == 0:
            month_end = today
        else:
            next_month = month_start.replace(day=28) + timedelta(days=4)
            month_end = next_month - timedelta(days=next_month.day)
        
        fines = Fine.objects.filter(date__gte=month_start, date__lte=month_end)
        monthly_data.append({
            'month': calendar.month_name[month_start.month],
            'year': month_start.year,
            'count': fines.count(),
            'amount': fines.aggregate(Sum('amount'))['amount__sum'] or 0
        })
    
    # Топ-5 владельцев с наибольшими штрафами
    top_owners = Owner.objects.annotate(
        fines_count=Count('fine'),
        fines_total=Sum('fine__amount')
    ).order_by('-fines_total')[:5]
    
    context = {
        'total_vehicles': total_vehicles,
        'total_owners': total_owners,
        'active_registrations': active_registrations,
        'total_fines': total_fines,
        'total_fines_amount': total_fines_amount,
        'unpaid_fines': unpaid_fines,
        'unpaid_fines_amount': unpaid_fines_amount,
        'paid_fines': paid_fines,
        'paid_fines_amount': paid_fines_amount,
        'appealed_fines': appealed_fines,
        'appealed_fines_amount': appealed_fines_amount,
        'top_vehicles': top_vehicles,
        'top_owners': top_owners,
        'monthly_data': monthly_data,
    }
    
    return render(request, 'vehicles/reports.html', context)