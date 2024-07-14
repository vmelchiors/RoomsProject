from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.models import Teacher, Discipline, PhysicalSpace, Allocation
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
        # Se o login falhar
        messages.error(request, 'Usuário ou senha inválidos')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password == password_confirm:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Nome de usuário já existe')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email já está registrado')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('login')
        else:
            messages.error(request, 'As senhas não coincidem')

    return render(request, 'register.html')
def dashboard_view(request):
    return render(request, 'dashboard.html')

def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teacher_list.html', {'teachers': teachers})

def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    return render(request, 'teacher_detail.html', {'teacher': teacher})

def teacher_create(request):
    if request.method == 'POST':
        siape = request.POST.get('siape')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if siape and first_name and last_name:
            Teacher.objects.create(siape=siape, first_name=first_name, last_name=last_name)
            return redirect('teacher_list')
        else:
            error_message = "Por favor, preencha todos os campos obrigatórios."
            return render(request, 'teacher_form.html', {'error': error_message})

    return render(request, 'teacher_form.html')

def teacher_update(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        siape = request.POST.get('siape')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if siape and first_name and last_name:
            teacher.siape = siape
            teacher.first_name = first_name
            teacher.last_name = last_name
            teacher.save()
            return redirect('teacher_list')
        else:
            error_message = "Por favor, preencha todos os campos obrigatórios."
            return render(request, 'teacher_form.html', {'teacher': teacher, 'error': error_message})

    return render(request, 'teacher_form.html', {'teacher': teacher})
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        return redirect('teacher_list')
    return render(request, 'teacher_confirm_delete.html', {'teacher': teacher})

def discipline_list(request):
    disciplines = Discipline.objects.all()
    return render(request, 'discipline_list.html', {'disciplines': disciplines})

def discipline_detail(request, pk):
    discipline = get_object_or_404(Discipline, pk=pk)
    return render(request, 'discipline_detail.html', {'discipline': discipline})
def discipline_create(request):
    if request.method == 'POST':
        discipline_name = request.POST.get('discipline_name')
        discipline_code = request.POST.get('discipline_code')
        discipline_mode = request.POST.get('discipline_mode')
        discipline_course = request.POST.get('discipline_course')

        if discipline_name and discipline_code and discipline_course:
            Discipline.objects.create(
                discipline_name=discipline_name,
                discipline_code=discipline_code,
                discipline_mode=discipline_mode,
                discipline_course=discipline_course
            )
            return redirect('discipline_list')
        else:
            error_message = "Por favor, preencha todos os campos obrigatórios."
            return render(request, 'discipline_form.html', {'error': error_message})

    return render(request, 'discipline_form.html')

def discipline_update(request, pk):
    discipline = get_object_or_404(Discipline, pk=pk)
    if request.method == 'POST':
        discipline_name = request.POST.get('discipline_name')
        discipline_code = request.POST.get('discipline_code')
        discipline_mode = request.POST.get('discipline_mode')

        if discipline_name and discipline_code:
            discipline.discipline_name = discipline_name
            discipline.discipline_code = discipline_code
            discipline.discipline_mode = discipline_mode
            discipline.save()
            return redirect('discipline_list')
        else:
            error_message = "Por favor, preencha todos os campos obrigatórios."
            return render(request, 'discipline_form.html', {'discipline': discipline, 'error': error_message})

    return render(request, 'discipline_form.html', {'discipline': discipline})
def discipline_delete(request, pk):
    discipline = get_object_or_404(Discipline, pk=pk)
    if request.method == 'POST':
        discipline.delete()
        return redirect('discipline_list')
    return render(request, 'discipline_confirm_delete.html', {'discipline': discipline})

def space_list(request):
    spaces = PhysicalSpace.objects.all()
    return render(request, 'space_list.html', {'spaces': spaces})

def space_detail(request, pk):
    space = get_object_or_404(PhysicalSpace, pk=pk)
    return render(request, 'space_detail.html', {'space': space})

def space_create(request):
    if request.method == 'POST':
        space_floor = request.POST.get('space_floor')
        space_number = request.POST.get('space_number')
        space_block = request.POST.get('space_block')
        space_type = request.POST.get('space_type')
        PhysicalSpace.objects.create(space_floor=space_floor, space_number=space_number, space_block=space_block, space_type=space_type)
        return redirect('space_list')
    return render(request, 'space_form.html')

def space_update(request, pk):
    space = get_object_or_404(PhysicalSpace, pk=pk)
    if request.method == 'POST':
        space_floor = request.POST.get('space_floor')
        space_number = request.POST.get('space_number')
        space_block = request.POST.get('space_block')
        space_type = request.POST.get('space_type')
        space.space_floor = space_floor
        space.space_number = space_number
        space.space_block = space_block
        space.space_type = space_type
        space.save()
        return redirect('space_list')
    return render(request, 'space_form.html', {'space': space})

def space_delete(request, pk):
    space = get_object_or_404(PhysicalSpace, pk=pk)
    if request.method == 'POST':
        space.delete()
        return redirect('space_list')
    return render(request, 'space_confirm_delete.html', {'space': space})

def allocation_list(request):
    allocations = Allocation.objects.all()
    return render(request, 'allocation_list.html', {'allocations': allocations})

def allocation_detail(request, pk):
    allocation = get_object_or_404(Allocation, pk=pk)
    return render(request, 'allocation_detail.html', {'allocation': allocation})

def allocation_create(request):
    teachers = Teacher.objects.all()
    disciplines = Discipline.objects.all()
    spaces = PhysicalSpace.objects.all()
    dias_da_semana = Allocation.DIAS_DA_SEMANA
    horarios = Allocation.HORARIOS

    if request.method == 'POST':
        teacher_id = request.POST.get('teacher')
        discipline_id = request.POST.get('discipline')
        space_id = request.POST.get('space')
        days_week = request.POST.get('days_week')
        timetable = request.POST.get('timetable')

        teacher = get_object_or_404(Teacher, pk=teacher_id)
        discipline = get_object_or_404(Discipline, pk=discipline_id)
        space = get_object_or_404(PhysicalSpace, pk=space_id)

        Allocation.objects.create(teacher=teacher, discipline=discipline, space=space, days_week=days_week, timetable=timetable)
        return redirect('allocation_list')

    context = {
        'teachers': teachers,
        'disciplines': disciplines,
        'spaces': spaces,
        'dias_da_semana': dias_da_semana,
        'horarios': horarios,
    }
    return render(request, 'allocation_form.html', context)

def allocation_update(request, pk):
    allocation = get_object_or_404(Allocation, pk=pk)
    teachers = Teacher.objects.all()
    disciplines = Discipline.objects.all()
    spaces = PhysicalSpace.objects.all()

    if request.method == 'POST':
        teacher_id = request.POST.get('teacher')
        discipline_id = request.POST.get('discipline')
        space_id = request.POST.get('space')
        days_week = request.POST.get('days_week')
        timetable = request.POST.get('timetable')

        teacher = get_object_or_404(Teacher, pk=teacher_id)
        discipline = get_object_or_404(Discipline, pk=discipline_id)
        space = get_object_or_404(PhysicalSpace, pk=space_id)

        allocation.teacher = teacher
        allocation.discipline = discipline
        allocation.space = space
        allocation.days_week = days_week
        allocation.timetable = timetable
        allocation.save()

        return redirect('allocation_list')

    return render(request, 'allocation_form.html', {'allocation': allocation, 'teachers': teachers, 'disciplines': disciplines, 'spaces': spaces})

def allocation_delete(request, pk):
    allocation = get_object_or_404(Allocation, pk=pk)

    if request.method == 'POST':
        allocation.delete()
        return redirect('allocation_list')

    return render(request, 'allocation_confirm_delete.html', {'allocation': allocation})

from django.http import JsonResponse

def generate_ensalamento(request):
    if request.method == 'POST':
        # Lógica para gerar o ensalamento
        # Por exemplo, chamar uma função que realiza o ensalamento
        # e retornar uma resposta de sucesso
        success = True  # Substitua pela lógica real

        if success:
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error'}, status=500)
    else:
        return JsonResponse({'status': 'error'}, status=405)
