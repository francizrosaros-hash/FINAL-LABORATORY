
from django.contrib import admin
from .models import Employee, Department, Position, Attendance, LeaveRequest

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'description')
    search_fields = ('title',)
    list_filter = ('department',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'position', 'department', 'is_active')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('department', 'position', 'is_active', 'date_joined')
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'address')
        }),
        ('Employment Details', {
            'fields': ('position', 'department', 'salary', 'date_joined', 'is_active')
        }),
    )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'check_in', 'check_out', 'status')
    search_fields = ('employee__first_name', 'employee__last_name')
    list_filter = ('status', 'date')
    date_hierarchy = 'date'


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'status', 'created_at')
    search_fields = ('employee__first_name', 'employee__last_name')
    list_filter = ('status', 'leave_type')
    date_hierarchy = 'start_date'
