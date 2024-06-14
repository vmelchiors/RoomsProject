from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.email

class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    siape = models.CharField(max_length=8)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Discipline(models.Model):
    discipline_id = models.AutoField(primary_key=True)
    discipline_name = models.CharField(max_length=30)
    discipline_code = models.CharField(max_length=10)

    def __str__(self):
        return self.discipline_name


class PhysicalSpace(models.Model):
    space_id = models.AutoField(primary_key=True)
    space_floor = models.IntegerField()
    space_number = models.IntegerField()
    space_block = models.CharField(max_length=1)
    space_type = models.BooleanField()

    def __str__(self):
        return f'{self.space_block} - {self.space_number}'


class Allocation(models.Model):
    allocation_id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    space = models.ForeignKey(PhysicalSpace, on_delete=models.CASCADE)
    days_week = models.CharField(max_length=10)
    timetable = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.teacher} - {self.discipline} - {self.space} - {self.timetable}'
