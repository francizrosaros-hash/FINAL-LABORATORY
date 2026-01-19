from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # AJAX endpoints
    path('ajax/get-positions/', views.get_positions_by_department, name='get_positions'),
    
    # Employee URLs
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_add, name='employee_add'),
    path('employees/edit/<int:pk>/', views.employee_edit, name='employee_edit'),
    path('employees/delete/<int:pk>/', views.employee_delete, name='employee_delete'),
    path('employees/<int:pk>/', views.employee_detail, name='employee_detail'),
    
    # Attendance URLs
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/add/', views.attendance_add, name='attendance_add'),
    path('attendance/edit/<int:pk>/', views.attendance_edit, name='attendance_edit'),
    path('attendance/delete/<int:pk>/', views.attendance_delete, name='attendance_delete'),
    
    # Leave Request URLs
    path('leaves/', views.leave_list, name='leave_list'),
    path('leaves/add/', views.leave_add, name='leave_add'),
    path('leaves/edit/<int:pk>/', views.leave_edit, name='leave_edit'),
    path('leaves/delete/<int:pk>/', views.leave_delete, name='leave_delete'),
    path('leaves/approve/<int:pk>/', views.leave_approve, name='leave_approve'),
    path('leaves/reject/<int:pk>/', views.leave_reject, name='leave_reject'),
    
    # Authentication URLs
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]
