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


from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def download_allocations_pdf(request):
    allocations = Allocation.objects.all()
    course = request.GET.get('course')

    if course:
        allocations = allocations.filter(discipline__discipline_course__icontains=course)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="allocations.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, "Lista de Alocações")

    p.setFont("Helvetica", 12)
    y = height - 80

    for allocation in allocations:
        p.drawString(100, y, f"Professor: {allocation.teacher}")
        y -= 15
        p.drawString(100, y, f"Disciplina: {allocation.discipline}")
        y -= 15
        p.drawString(100, y, f"Sala: {allocation.space}")
        y -= 15
        p.drawString(100, y, f"Dia da Semana: {allocation.get_days_week_display()}")
        y -= 15
        p.drawString(100, y, f"Horário: {allocation.get_timetable_display()}")
        y -= 25
        if y < 100:
            p.showPage()
            p.setFont("Helvetica", 12)
            y = height - 50

    p.showPage()
    p.save()
    return response

