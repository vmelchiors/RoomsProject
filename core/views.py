from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import csv
from django.shortcuts import render
from .models import Allocation, Discipline
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def index(request):
    return render(request, 'index.html')

def allocation_list(request):
    allocations = Allocation.objects.all()
    courses = Discipline.objects.values_list('discipline_course', flat=True).distinct()

    course = request.GET.get('course')

    if course:
        allocations = allocations.filter(discipline__discipline_course__icontains=course)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        allocation_list = []
        for allocation in allocations:
            allocation_list.append({
                'teacher': str(allocation.teacher),
                'discipline': str(allocation.discipline),
                'space': str(allocation.space),
                'days_week': allocation.get_days_week_display(),
                'timetable': allocation.get_timetable_display(),
            })
        return JsonResponse({'allocations': allocation_list})
    else:
        return render(request, 'rooms.html', {'allocations': allocations, 'courses': courses})


def download_allocations_pdf(request):
    allocations = Allocation.objects.all()

    course = request.GET.get('course')

    if course:
        allocations = allocations.filter(discipline__discipline_course__icontains=course)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="allocations.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    p.drawString(100, height - 100, "Lista de Alocações")
    y = height - 120

    for allocation in allocations:
        p.drawString(100, y, f"Professor: {allocation.teacher}")
        p.drawString(200, y, f"Disciplina: {allocation.discipline}")
        p.drawString(300, y, f"Sala: {allocation.space}")
        p.drawString(400, y, f"Dia da Semana: {allocation.get_days_week_display()}")
        p.drawString(500, y, f"Horário: {allocation.get_timetable_display()}")
        y -= 20

    p.showPage()
    p.save()
    return response
