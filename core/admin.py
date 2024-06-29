from django.contrib import admin
from .models import User, Teacher, Discipline, PhysicalSpace, Allocation

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_id', 'siape', 'first_name', 'last_name')
    search_fields = ('first_name', 'last_name', 'siape')

@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('discipline_id', 'discipline_name', 'discipline_code')
    search_fields = ('discipline_name', 'discipline_code')

@admin.register(PhysicalSpace)
class PhysicalSpaceAdmin(admin.ModelAdmin):
    list_display = ('space_id', 'space_floor', 'space_number', 'space_block', 'space_type')
    search_fields = ('space_floor', 'space_number', 'space_block')

@admin.register(Allocation)
class AllocationAdmin(admin.ModelAdmin):
    list_display = ('allocation_id', 'teacher', 'discipline', 'space', 'days_week', 'timetable')
    search_fields = ('teacher__first_name', 'teacher__last_name', 'discipline__discipline_name', 'space__space_number')

