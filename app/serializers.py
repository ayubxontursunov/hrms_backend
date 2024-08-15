from rest_framework import serializers
from .models import *

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'email']
#
#     def create(self, validated_data):
#         user = User.objects.create(**validated_data)
#         return user



from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password
import random
import string

from django.contrib.auth import authenticate
from .models import User  # Adjust import if using a custom user model

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from .models import User
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from .models import User
from rest_framework import serializers
from .models import Employee, Department, Division, Team, Position

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")

        # Check password
        if not check_password(password, user.password_hash):
            raise serializers.ValidationError("Invalid credentials")

        # Add user instance to validated data
        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)  # Optional on creation

    class Meta:
        model = User
        fields = ['id', 'employee', 'username', 'email', 'password', 'is_admin']

    def create(self, validated_data):
        # Extract the password and remove it from validated_data
        password = validated_data.pop('password', None)
        # Generate a random password if none is provided
        if not password:
            password = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_uppercase, k=12))
        # Create the user instance
        user = super().create(validated_data)
        # Set the password hash and save the user
        user.password_hash = make_password(password)
        user.save()
        # Return the user instance and the generated password
        return user, password

    def update(self, instance, validated_data):
        # Extract the password and remove it from validated_data
        password = validated_data.pop('password', None)
        # Update the user instance
        user = super().update(instance, validated_data)
        # Set the new password hash if provided
        if password:
            user.password_hash = make_password(password)
            user.save()
        return user


# class DepartmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Department
#         fields = '__all__'
#
# class DivisionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Division
#         fields = '__all__'
#
# class TeamSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Team
#         fields = '__all__'
#
# class PositionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Position
#         fields = '__all__'

#
# class DepartmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Department
#         fields = ['id', 'department_name']
#
#
# class DivisionSerializer(serializers.ModelSerializer):
#     department = DepartmentSerializer()
#
#     class Meta:
#         model = Division
#         fields = ['id', 'division_name', 'department']
#
#
# class TeamSerializer(serializers.ModelSerializer):
#     division = DivisionSerializer()
#
#     class Meta:
#         model = Team
#         fields = ['id', 'team_name', 'division']
#
#
# class PositionSerializer(serializers.ModelSerializer):
#     department = DepartmentSerializer()
#
#     class Meta:
#         model = Position
#         fields = ['id', 'position_name', 'job_description', 'department']


# class EmployeeSerializer(serializers.ModelSerializer):
#     department = DepartmentSerializer()
#     division = DivisionSerializer()
#     team = TeamSerializer()
#     position = PositionSerializer()
#     # class Meta:
#     #     model = Employee
#         # fields = '__all__'
#     class Meta:
#         model = Employee
#         fields = ['id', 'user', 'first_name', 'last_name', 'patronymic', 'profile_photo', 'status', 'address',
#                       'phone_number', 'nationality', 'birthdate', 'education', 'marital_status', 'department',
#                       'division', 'team', 'position', 'created_at', 'updated_at']



# class EmployeeSerializer(serializers.ModelSerializer):
#     department = DepartmentSerializer()
#     division = DivisionSerializer()
#     team = TeamSerializer()
#     position = PositionSerializer()
#
#     class Meta:
#         model = Employee
#         fields = ['id',  'first_name', 'last_name', 'patronymic', 'profile_photo', 'address',
#                   'phone_number', 'nationality', 'birthdate', 'education', 'marital_status', 'department', 'division',
#                   'team', 'position', 'created_at', 'updated_at']
#
#     def create(self, validated_data):
#         department_data = validated_data.pop('department')
#         division_data = validated_data.pop('division')
#         team_data = validated_data.pop('team')
#         position_data = validated_data.pop('position')
#
#         # Handle Department creation
#         department, created = Department.objects.get_or_create(**department_data)
#
#         # Handle Division creation
#         division_data['department'] = department
#         division, created = Division.objects.get_or_create(**division_data)
#
#         # Handle Team creation
#         team_data['division'] = division
#         team, created = Team.objects.get_or_create(**team_data)
#
#         # Handle Position creation
#         position_data['department'] = department
#         position, created = Position.objects.get_or_create(**position_data)
#
#         # Create Employee
#         employee = Employee.objects.create(
#             **validated_data,
#             department=department,
#             division=division,
#             team=team,
#             position=position
#         )
#         return employee
#
#     def update(self, instance, validated_data):
#         department_data = validated_data.pop('department', None)
#         division_data = validated_data.pop('division', None)
#         team_data = validated_data.pop('team', None)
#         position_data = validated_data.pop('position', None)
#
#         if department_data:
#             # Handle Department update or create
#             department, created = Department.objects.update_or_create(id=instance.department.id,
#                                                                       defaults=department_data)
#             instance.department = department
#
#         if division_data:
#             # Handle Division update or create
#             division_data['department'] = instance.department
#             division, created = Division.objects.update_or_create(id=instance.division.id, defaults=division_data)
#             instance.division = division
#
#         if team_data:
#             # Handle Team update or create
#             team_data['division'] = instance.division
#             team, created = Team.objects.update_or_create(id=instance.team.id, defaults=team_data)
#             instance.team = team
#
#         if position_data:
#             # Handle Position update or create
#             position_data['department'] = instance.department
#             position, created = Position.objects.update_or_create(id=instance.position.id, defaults=position_data)
#             instance.position = position
#
#         # Update Employee
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
#
#         return instance


# class EmployeeSerializer(serializers.ModelSerializer):
#     department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
#     division = serializers.PrimaryKeyRelatedField(queryset=Division.objects.all())
#     team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
#     position = serializers.PrimaryKeyRelatedField(queryset=Position.objects.all())
#
#     class Meta:
#         model = Employee
#         fields = ['id', 'first_name', 'last_name', 'patronymic', 'profile_photo', 'address',
#                   'phone_number', 'nationality', 'birthdate', 'education', 'marital_status',
#                   'department', 'division', 'team', 'position', 'created_at', 'updated_at']
#
#     def create(self, validated_data):
#         # Extract IDs
#         department_id = validated_data.pop('department')
#         division_id = validated_data.pop('division')
#         team_id = validated_data.pop('team')
#         position_id = validated_data.pop('position')
#
#         # Get related objects
#         department = Department.objects.get(id=department_id)
#         division = Division.objects.get(id=division_id)
#         team = Team.objects.get(id=team_id)
#         position = Position.objects.get(id=position_id)
#
#         # Create Employee
#         employee = Employee.objects.create(
#             **validated_data,
#             department=department,
#             division=division,
#             team=team,
#             position=position
#         )
#         return employee
#
#     def update(self, instance, validated_data):
#         # Extract IDs
#         department_id = validated_data.pop('department', None)
#         division_id = validated_data.pop('division', None)
#         team_id = validated_data.pop('team', None)
#         position_id = validated_data.pop('position', None)
#
#         if department_id is not None:
#             department = Department.objects.get(id=department_id)
#             instance.department = department
#
#         if division_id is not None:
#             division = Division.objects.get(id=division_id)
#             instance.division = division
#
#         if team_id is not None:
#             team = Team.objects.get(id=team_id)
#             instance.team = team
#
#         if position_id is not None:
#             position = Position.objects.get(id=position_id)
#             instance.position = position
#
#         # Update Employee
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
#
#         return instance

from rest_framework import serializers
from .models import Employee, Department, Division, Team, Position

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department_name']

class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = ['id', 'division_name', 'department']

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'team_name', 'division']

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'position', 'duty', 'department']

class EmployeeSerializer(serializers.ModelSerializer):
    # Use PrimaryKeyRelatedField to accept IDs for related fields
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    division = serializers.PrimaryKeyRelatedField(queryset=Division.objects.all())
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    position = serializers.PrimaryKeyRelatedField(queryset=Position.objects.all())

    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'patronymic', 'profile_photo', 'address',
                  'phone_number', 'nationality', 'birthdate', 'education', 'marital_status',
                  'department', 'division', 'team', 'position', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Fetch the related objects by their IDs
        department = validated_data.pop('department')
        division = validated_data.pop('division')
        team = validated_data.pop('team')
        position = validated_data.pop('position')

        department_instance = Department.objects.get(id=department.id)
        division_instance = Division.objects.get(id=division.id)
        team_instance = Team.objects.get(id=team.id)
        position_instance = Position.objects.get(id=position.id)

        # Create and return the Employee instance
        employee = Employee.objects.create(
            **validated_data,
            department=department_instance,
            division=division_instance,
            team=team_instance,
            position=position_instance
        )
        return employee

    def update(self, instance, validated_data):
        # Update related fields
        department = validated_data.pop('department', None)
        division = validated_data.pop('division', None)
        team = validated_data.pop('team', None)
        position = validated_data.pop('position', None)

        if department is not None:
            instance.department = Department.objects.get(id=department.id)
        if division is not None:
            instance.division = Division.objects.get(id=division.id)
        if team is not None:
            instance.team = Team.objects.get(id=team.id)
        if position is not None:
            instance.position = Position.objects.get(id=position.id)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    def to_representation(self, instance):
        # Customize the representation of the data for GET requests
        representation = super().to_representation(instance)
        representation['department'] = DepartmentSerializer(instance.department).data
        representation['division'] = DivisionSerializer(instance.division).data
        representation['team'] = TeamSerializer(instance.team).data
        representation['position'] = PositionSerializer(instance.position).data
        return representation



class EmployeePositionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePositionHistory
        fields = '__all__'


# class RoleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Role
#         fields = '__all__'

# class UserRoleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserRole
#         fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'


class EmployeeDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeDocument
        fields = '__all__'


class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = '__all__'


class EmployeeTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeTraining
        fields = '__all__'


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'
