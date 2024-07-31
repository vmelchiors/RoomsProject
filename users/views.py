from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.models import Teacher, Discipline, PhysicalSpace, Allocation
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db import IntegrityError


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

@login_required
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

@login_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teacher_list.html', {'teachers': teachers})

@login_required
def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    return render(request, 'teacher_detail.html', {'teacher': teacher})

@login_required
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

@login_required
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

@login_required
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        return redirect('teacher_list')
    return render(request, 'teacher_confirm_delete.html', {'teacher': teacher})

@login_required
def discipline_list(request):
    disciplines = Discipline.objects.all()
    return render(request, 'discipline_list.html', {'disciplines': disciplines})

@login_required
def discipline_detail(request, pk):
    discipline = get_object_or_404(Discipline, pk=pk)
    return render(request, 'discipline_detail.html', {'discipline': discipline})

@login_required
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

@login_required
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

@login_required
def discipline_delete(request, pk):
    discipline = get_object_or_404(Discipline, pk=pk)
    if request.method == 'POST':
        discipline.delete()
        return redirect('discipline_list')
    return render(request, 'discipline_confirm_delete.html', {'discipline': discipline})

@login_required
def space_list(request):
    spaces = PhysicalSpace.objects.all()
    return render(request, 'space_list.html', {'spaces': spaces})

@login_required
def space_detail(request, pk):
    space = get_object_or_404(PhysicalSpace, pk=pk)
    return render(request, 'space_detail.html', {'space': space})

@login_required
def space_create(request):
    if request.method == 'POST':
        space_floor = request.POST.get('space_floor')
        space_number = request.POST.get('space_number')
        space_block = request.POST.get('space_block')
        space_type = request.POST.get('space_type')

        try:
            PhysicalSpace.objects.create(
                space_floor=space_floor,
                space_number=space_number,
                space_block=space_block,
                space_type=space_type
            )
            return redirect('space_list')
        except Exception as e:
            return render(request, 'space_form.html', {'error': str(e)})

    return render(request, 'space_form.html')

@login_required
def space_update(request, pk):
    space = get_object_or_404(PhysicalSpace, pk=pk)

    if request.method == 'POST':
        space_floor = request.POST.get('space_floor')
        space_number = request.POST.get('space_number')
        space_block = request.POST.get('space_block')
        space_type = request.POST.get('space_type')

        try:
            space.space_floor = space_floor
            space.space_number = space_number
            space.space_block = space_block
            space.space_type = space_type
            space.save()
            return redirect('space_list')
        except Exception as e:
            return render(request, 'space_form.html', {'space': space, 'error': str(e)})

    return render(request, 'space_form.html', {'space': space})

@login_required
def space_delete(request, pk):
    space = get_object_or_404(PhysicalSpace, pk=pk)
    if request.method == 'POST':
        space.delete()
        return redirect('space_list')
    return render(request, 'space_confirm_delete.html', {'space': space})

@login_required
def allocation_list(request):
    allocations = Allocation.objects.all()
    return render(request, 'allocation_list.html', {'allocations': allocations})

@login_required
def allocation_detail(request, pk):
    allocation = get_object_or_404(Allocation, pk=pk)
    return render(request, 'allocation_detail.html', {'allocation': allocation})

@login_required
def allocation_create(request):
    teachers = Teacher.objects.all()
    disciplines = Discipline.objects.all()
    dias_da_semana = Allocation.DIAS_DA_SEMANA
    horarios = Allocation.HORARIOS
    spaces = PhysicalSpace.objects.all()

    if request.method == 'POST':
        teacher_id = request.POST.get('teacher')
        discipline_id = request.POST.get('discipline')
        days_week = request.POST.get('days_week')
        timetable = request.POST.get('timetable')
        space_id = request.POST.get('space')

        teacher = get_object_or_404(Teacher, pk=teacher_id)
        discipline = get_object_or_404(Discipline, pk=discipline_id)
        space = get_object_or_404(PhysicalSpace, pk=space_id) if space_id else None

        try:
            Allocation.objects.create(
                teacher=teacher,
                discipline=discipline,
                space=space,
                days_week=days_week,
                timetable=timetable
            )
            return redirect('allocation_list')
        except IntegrityError:
            error_message = 'Já existe uma alocação com este horário.'
            context = {
                'teachers': teachers,
                'disciplines': disciplines,
                'spaces': spaces,
                'dias_da_semana': dias_da_semana,
                'horarios': horarios,
                'error': error_message,
            }
            return render(request, 'allocation_form.html', context)

    context = {
        'teachers': teachers,
        'disciplines': disciplines,
        'spaces': spaces,
        'dias_da_semana': dias_da_semana,
        'horarios': horarios,
    }
    return render(request, 'allocation_form.html', context)

@login_required
def allocation_update(request, pk):
    allocation = get_object_or_404(Allocation, pk=pk)
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

        allocation.teacher = teacher
        allocation.discipline = discipline
        allocation.space = space
        allocation.days_week = days_week
        allocation.timetable = timetable
        allocation.save()

        return redirect('allocation_list')

    context = {
        'allocation': allocation,
        'teachers': teachers,
        'disciplines': disciplines,
        'spaces': spaces,
        'dias_da_semana': dias_da_semana,
        'horarios': horarios,
    }
    return render(request, 'allocation_form.html', context)

@login_required
def allocation_delete(request, pk):
    allocation = get_object_or_404(Allocation, pk=pk)

    if request.method == 'POST':
        allocation.delete()
        return redirect('allocation_list')

    return render(request, 'allocation_confirm_delete.html', {'allocation': allocation})

from django.http import JsonResponse
from core.models import Teacher, Discipline, PhysicalSpace, Allocation
from sklearn.tree import DecisionTreeClassifier
import pickle
from pathlib import Path
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent

file_path = BASE_DIR / 'Predict' / 'ensalamento.pkl'

with open(file_path, 'rb') as f:
    x_drying_training, y_drying_training, x_drying_test, y_drying_test = pickle.load(f)

tree_drying = DecisionTreeClassifier(criterion='entropy', random_state=0)
tree_drying.fit(x_drying_training, y_drying_training)


HORARIOS_MAP = {
    '08:00': 0, '09:00': 1, '10:00': 2, '11:00': 3, '12:00': 4, '13:00': 5,
    '14:00': 6, '15:00': 7, '16:00': 8, '17:00': 9, '18:00': 10, '19:00': 11,
    '20:00': 12, '21:00': 13
}


def days_to_binary(days_week):
    days_map = {'SEG': 0, 'TER': 1, 'QUA': 2, 'QUI': 3, 'SEX': 4, 'SAB': 5}
    binary_list = [0] * 6
    if days_week in days_map:
        binary_list[days_map[days_week]] = 1
    return binary_list

def drying_predict(time, days_week):

    time_value = HORARIOS_MAP.get(time, -1)

    days_list = days_to_binary(days_week)

    input_data = np.array([[time_value] + days_list])

    prediction = tree_drying.predict(input_data)
    return prediction

@login_required
def generate_ensalamento(request):
    if request.method == 'POST':
        try:
            allocations = Allocation.objects.all()
            for allocation in allocations:
                time = allocation.timetable
                days_week = allocation.days_week

                print(f"Predicting for time={time}, days_week={days_week}")

                prediction = drying_predict(time, days_week)
                print(f"Prediction result: {prediction}")

                predicted_space = prediction[0]
                try:

                    space_number = int(predicted_space.split('-')[0])
                    space_block = predicted_space.split('-')[1]

                    if len(space_block) != 1 or not space_block.isalpha():
                        raise ValueError(f"Invalid space block format: {space_block}")

                    space = PhysicalSpace.objects.get(space_number=space_number, space_block=space_block)
                    print(f"Found space: {space}")
                except PhysicalSpace.DoesNotExist:
                    print(f"PhysicalSpace with number {space_number} and block {space_block} does not exist.")
                    continue
                except ValueError as ve:
                    print(f"ValueError: {ve}")
                    continue

                allocation.space = space
                allocation.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(f"Error occurred: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error'}, status=405)
