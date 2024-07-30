from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from core.models import Discipline
from core.models import Teacher
from core.models import PhysicalSpace
from core.models import Allocation
class LoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin')

    def test_login_view_success(self):
        url = reverse('login')
        data = {
            'username': 'admin',
            'password': 'admin'
        }

        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_view_failure(self):
        url = reverse('login')
        data = {
            'username': 'azul',
            'password': 'verde'
        }
        response = self.client.post(url, data)
        self.assertTemplateUsed(response, 'login.html')
        self.assertIn('Usuário ou senha inválidos', response.content.decode())
        self.assertFalse(response.wsgi_request.user.is_authenticated)

class LogoutViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin')

    def test_logout_view(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('logout'))

        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(response, reverse('login'))

class RegisterViewTest(TestCase):
    def setUp(self):
        self.url = reverse('register')
        self.login_url = reverse('login')

    def test_register_view_success(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'password_confirm': 'password123'
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, self.login_url)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_view_username_exists(self):
        User.objects.create_user(username='existinguser', email='existinguser@example.com', password='password123')
        data = {
            'username': 'existinguser',
            'email': 'newemail@example.com',
            'password': 'password123',
            'password_confirm': 'password123'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Nome de usuário já existe', response.content.decode())

    def test_register_view_email_exists(self):
        User.objects.create_user(username='newuser', email='existingemail@example.com', password='password123')
        data = {
            'username': 'newuser2',
            'email': 'existingemail@example.com',
            'password': 'password123',
            'password_confirm': 'password123'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Email já está registrado', response.content.decode())

    def test_register_view_passwords_do_not_match(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'password_confirm': 'differentpassword'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('As senhas não coincidem', response.content.decode())

class TeacherCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin')

    def teacher_create_view(self):
        url = reverse('teacher_create')
        data = {
            'siape': '889256',
            'first_name': 'XIFU',
            'last_name': 'OUUOR',
        }
        self.client.force_login(self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Discipline.objects.count(), 1)

        teacher = Teacher.objects.first()
        self.assertEqual(teacher.siape, '889256')
        self.assertEqual(teacher.first_name, 'XIFU')
        self.assertEqual(teacher.last_name, 'OUUOR')

        self.assertRedirects(response, reverse('teacher_list'))

class TeacherUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin')
        self.teacher = Teacher.objects.create(
            siape='889256',
            first_name='XIFU',
            last_name='OUUOR',
        )

    def teacher_update_view(self):
        url = reverse('teacher_update', args=[self.teacher.pk])
        data = {
            'siape': '000658',
            'first_name': 'POU',
            'last_name': 'LACR'
        }
        self.client.force_login(self.user)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.siape, '000658')
        self.assertEqual(self.teacher.first_name, 'POU')
        self.assertEqual(self.teacher.last_name, 'LACR')

        self.assertRedirects(response, reverse('teacher_list'))

class TeacherDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin')
        self.teacher = Teacher.objects.create(
            siape='463589',
            first_name='XICO',
            last_name='LIRO'
        )

    def test_teacher_delete_view(self):
        url = reverse('teacher_delete', args=[self.teacher.pk])
        self.client.force_login(self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Teacher.objects.count(), 0)
        self.assertRedirects(response, reverse('teacher_list'))
        self.assertFalse(Teacher.objects.filter(pk=self.teacher.pk).exists())

class DisciplineCreateViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin')
    def test_discipline_create_view(self):
        url = reverse('discipline_create')
        data = {
            'discipline_name': 'Matematica',
            'discipline_code': 'TESTE123',
            'discipline_mode': False,
            'discipline_course': 'Eng Soft'
        }

        self.client.force_login(self.user)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Discipline.objects.count(), 1)

        discipline = Discipline.objects.first()
        self.assertEqual(discipline.discipline_name, 'Matematica')
        self.assertEqual(discipline.discipline_code, 'TESTE123')
        self.assertEqual(discipline.discipline_mode, False)
        self.assertEqual(discipline.discipline_course, 'Eng Soft')

        self.assertRedirects(response, reverse('discipline_list'))

class DisciplineUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin')
        self.discipline = Discipline.objects.create(
            discipline_name=' Disciplina',
            discipline_code='TESTE123',
            discipline_mode=True,
            discipline_course='Quimica'
        )
    def test_discipline_update_view(self):
        url = reverse('discipline_update', args=[self.discipline.pk])
        data = {
            'discipline_name': 'Geografia',
            'discipline_code': 'GEO01',
            'discipline_mode': False,
            'discipline_course': 'Pedagogia'
        }
        self.client.force_login(self.user)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.discipline.refresh_from_db()
        self.assertEqual(self.discipline.discipline_name, 'Geografia')
        self.assertEqual(self.discipline.discipline_code, 'GEO01')
        self.assertEqual(self.discipline.discipline_mode, False)
        self.assertEqual(self.discipline.discipline_course, 'Pedagogia')

        self.assertRedirects(response, reverse('discipline_list'))

class DisciplineDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin')
        self.discipline = Discipline.objects.create(
            discipline_name='Musica',
            discipline_code='MU334',
            discipline_mode=True,
            discipline_course='Letras'
        )

    def test_discipline_delete_view(self):
        url = reverse('discipline_delete', args=[self.discipline.pk])
        self.client.force_login(self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Discipline.objects.count(), 0)
        self.assertRedirects(response, reverse('discipline_list'))
        self.assertFalse(Discipline.objects.filter(pk=self.discipline.pk).exists())

class PhysicalSpaceCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin')
        self.url = reverse('space_create')

    def test_physical_space_create_view_success(self):
        self.client.force_login(self.user)
        data = {
            'space_floor': '3',
            'space_number': '303',
            'space_block': 'A',
            'space_type': True
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('space_list'))
        self.assertTrue(PhysicalSpace.objects.filter(space_number='303').exists())

    def test_space_create_view_failure(self):
        data = {
            'space_number': '303',
            'space_block': 'A',
            'space_type': False  # Assuming '1' is for 'Laboratório'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)  # Ensure it renders the form again due to the error

class PhysicalSpaceUpdateViewTest(TestCase):
    def setUp(self):
        # Cria um espaço físico inicial para teste
        self.space = PhysicalSpace.objects.create(
            space_floor=1,
            space_number=101,
            space_block='A',
            space_type=True
        )
        self.url = reverse('space_update', kwargs={'pk': self.space.pk})
        self.space_list_url = reverse('space_list')

    def test_space_update_view_success(self):
        data = {
            'space_floor': 2,
            'space_number': 102,
            'space_block': 'B',
            'space_type': False
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, self.space_list_url)
        self.space.refresh_from_db()
        self.assertEqual(self.space.space_floor, 2)
        self.assertEqual(self.space.space_number, 102)
        self.assertEqual(self.space.space_block, 'B')
        self.assertFalse(self.space.space_type)

    def test_space_update_view_failure(self):
        data = {
            'space_floor': '',
            'space_number': 103,
            'space_block': 'C',
            'space_type': True
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)

class PhysicalSpaceDeleteViewTest(TestCase):
    def setUp(self):
        self.space = PhysicalSpace.objects.create(
            space_floor=1,
            space_number=101,
            space_block='A',
            space_type=True
        )
        self.url = reverse('space_delete', kwargs={'pk': self.space.pk})
        self.space_list_url = reverse('space_list')

    def test_space_delete_view_success(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, self.space_list_url)

class AllocationDetailViewTest(TestCase):
    def setUp(self):
            self.user = User.objects.create_user(username='admin', password='admin')
            self.url = reverse('space_create')

            self.teacher1 = Teacher.objects.create(siape='12345678', first_name='João', last_name='Silva')
            self.teacher2 = Teacher.objects.create(siape='87654321', first_name='Maria', last_name='Santos')

            self.discipline = Discipline.objects.create(
                discipline_name='Matemática',
                discipline_code='MAT101',
                discipline_mode=False,
                discipline_course='Engenharia'
            )

            self.physical_space = PhysicalSpace.objects.create(
                space_floor=1,
                space_number='102',
                space_block='A',
                space_type=False
            )

    def test_allocation_create_success(self):
        response = self.client.post('/allocation/add/', {
            'teacher': self.teacher2.pk,
            'discipline': self.discipline.pk,
            'days_week': 'TER',
            'timetable': '10:00',
            'space': self.physical_space.pk
        })

        allocation_exists = Allocation.objects.filter(
            teacher=self.teacher2,
            discipline=self.discipline,
            days_week='TER',
            timetable='10:00',
            space=self.physical_space
        ).exists()


class AllocationDeleteViewTest(TestCase):
    def setUp(self):
        # Criação de dados necessários para os testes
        self.user = User.objects.create_user(username='admin', password='admin')
        self.client.login(username='admin', password='admin')

        self.teacher = Teacher.objects.create(
            siape='12345678',
            first_name='Maria',
            last_name='Lopes'
        )

        self.discipline = Discipline.objects.create(
            discipline_name='Matemática',
            discipline_code='MAT101',
            discipline_mode=False,
            discipline_course='Bacharelado'
        )

        self.physical_space = PhysicalSpace.objects.create(
            space_number=101,
            space_block='A',
            space_floor=1 ,
            space_type=True
        )

        self.allocation = Allocation.objects.create(
            teacher=self.teacher,
            discipline=self.discipline,
            space=self.physical_space,
            days_week='SEG',
            timetable='08:00'
        )

    def test_allocation_delete_view_get(self):
        # Verifica se o GET retorna o template correto com a alocação
        response = self.client.get(reverse('allocation_delete', kwargs={'pk': self.allocation.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'allocation_confirm_delete.html')
        self.assertContains(response, 'Você tem certeza que deseja excluir')

    def test_allocation_delete_view_post(self):
        # Verifica se o POST exclui a alocação e redireciona para a lista
        response = self.client.post(reverse('allocation_delete', kwargs={'pk': self.allocation.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('allocation_list'))
        self.assertFalse(Allocation.objects.filter(pk=self.allocation.pk).exists())