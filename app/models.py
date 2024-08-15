from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.db import models
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token for {self.user.username}"




class Department(models.Model):
    department_name = models.CharField(max_length=100, null=False)
    parent_department = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='child_departments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.department_name




class Division(models.Model):
    division_name = models.CharField(max_length=100, null=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='divisions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.division_name

class Team(models.Model):
    team_name = models.CharField(max_length=100, null=False)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='teams')
    team_lead = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, related_name='lead_teams')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.team_name

class Position(models.Model):
    position = models.CharField(max_length=100, null=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='positions')
    duty = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.position

class Employee(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    patronymic = models.CharField(max_length=50, blank=True, null=True)
    profile_photo = models.ImageField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    marital_status = models.CharField(max_length=20, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='employees')
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True, related_name='employees')
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name='employees')
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, related_name='employees')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class User(models.Model):
    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(max_length=100, unique=True, null=False)
    password_hash = models.CharField(max_length=255, null=True)
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='user')
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    def __str__(self):
        return self.username

class EmployeePositionHistory(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='position_history')
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    start_date = models.DateField(null=False)
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# class Role(models.Model):
#     role_name = models.CharField(max_length=50, unique=True, null=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.role_name
#
# class UserRole(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roles')
#     role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='users')
#     assigned_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         unique_together = ('user', 'role')

class Document(models.Model):
    document_name = models.CharField(max_length=255, null=False)
    document_type = models.CharField(max_length=50, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    document_data = models.BinaryField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class EmployeeDocument(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='documents')
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='employee_documents')
    access_type = models.CharField(max_length=20, blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)

class Training(models.Model):
    training_name = models.CharField(max_length=255, null=False)
    coordinator = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='coordinated_trainings')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='trainings')
    start_date = models.DateField(null=False)
    end_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='created_trainings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class EmployeeTraining(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='trainings')
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name='employees')
    status = models.CharField(max_length=20, blank=True, null=True)
    completion_date = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = ('employee', 'training')

class Announcement(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='created_announcements')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leaves')
    leave_type = models.CharField(max_length=50, null=False)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    duration = models.IntegerField(blank=True, null=True)
    approval_status = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField(null=False)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

