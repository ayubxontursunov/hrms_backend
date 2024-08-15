from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'employees', views.EmployeeViewSet)
router.register(r'departments', views.DepartmentViewSet)
router.register(r'divisions', views.DivisionViewSet)
router.register(r'teams', views.TeamViewSet)
router.register(r'positions', views.PositionViewSet)
router.register(r'employee-position-history', views.EmployeePositionHistoryViewSet)
# router.register(r'roles', views.RoleViewSet)
# router.register(r'user-roles', views.UserRoleViewSet)
router.register(r'documents', views.DocumentViewSet)
router.register(r'employee-documents', views.EmployeeDocumentViewSet)
router.register(r'trainings', views.TrainingViewSet)
router.register(r'employee-trainings', views.EmployeeTrainingViewSet)
router.register(r'announcements', views.AnnouncementViewSet)
router.register(r'leaves', views.LeaveViewSet)
router.register(r'notifications', views.NotificationViewSet)
router.register(r'tokens', views.TokenViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('user/', views.UserCreateView.as_view(), name='user-create'),

    # Route for updating or deleting a user
    path('user/<int:user_id>/', views.UserCreateView.as_view(), name='user-detail'),
    path('login/', views.LoginView.as_view(), name='login'),
]


