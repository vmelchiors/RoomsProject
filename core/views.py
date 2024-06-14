from django.shortcuts import render

from django.shortcuts import render
from .models import Allocation

def index(request):
    return render(request, 'index.html')

def allocation_list(request):
    allocations = Allocation.objects.all()
    return render(request, 'rooms.html', {'allocations': allocations})
