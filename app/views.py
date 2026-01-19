from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from .models import Employee, Attendance, LeaveRequest, Position
from .forms import EmployeeForm, AttendanceForm, LeaveRequestForm, AdminRegistrationForm


def get_positions_by_department(request):
    """AJAX endpoint to get positions filtered by department"""
    department_id = request.GET.get('department_id')
    if department_id:
        positions = Position.objects.filter(department_id=department_id).values('id', 'title')
    else:
        positions = Position.objects.all().values('id', 'title')
    return JsonResponse(list(positions), safe=False)

def home(request):
    return render(request, 'base/home.html')

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('home')

class CustomLogoutView(LogoutView):
    next_page = 'home'

def register(request):
    if request.user.is_authenticated:
        return redirect('employee_list')
    
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Admin account created successfully! Please log in.')
            return redirect('login')
    else:
        form = AdminRegistrationForm()
    
    return render(request, 'base/register.html', {'form': form})

@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'base/employee_list.html', {'employees': employees})

@login_required
def employee_add(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'base/employee_form.html', {'form': form, 'title': 'Add Employee'})

@login_required
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'base/employee_form.html', {'form': form, 'title': 'Edit Employee'})

@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'base/employee_detail.html', {'employee': employee})

@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')
    return render(request, 'base/employee_confirm_delete.html', {'employee': employee})


# Attendance Views
@login_required
def attendance_list(request):
    attendances = Attendance.objects.select_related('employee').all()
    return render(request, 'base/attendance_list.html', {'attendances': attendances})

@login_required
def attendance_add(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance record added successfully!')
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'base/attendance_form.html', {'form': form, 'title': 'Add Attendance'})

@login_required
def attendance_edit(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance record updated successfully!')
            return redirect('attendance_list')
    else:
        form = AttendanceForm(instance=attendance)
    return render(request, 'base/attendance_form.html', {'form': form, 'title': 'Edit Attendance'})

@login_required
def attendance_delete(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        attendance.delete()
        messages.success(request, 'Attendance record deleted.')
        return redirect('attendance_list')
    return render(request, 'base/attendance_confirm_delete.html', {'attendance': attendance})


# Leave Request Views
@login_required
def leave_list(request):
    leaves = LeaveRequest.objects.select_related('employee').all()
    return render(request, 'base/leave_list.html', {'leaves': leaves})

@login_required
def leave_add(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Leave request submitted successfully!')
            return redirect('leave_list')
    else:
        form = LeaveRequestForm()
    return render(request, 'base/leave_form.html', {'form': form, 'title': 'Add Leave Request'})

@login_required
def leave_edit(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, instance=leave)
        if form.is_valid():
            form.save()
            messages.success(request, 'Leave request updated successfully!')
            return redirect('leave_list')
    else:
        form = LeaveRequestForm(instance=leave)
    return render(request, 'base/leave_form.html', {'form': form, 'title': 'Edit Leave Request'})

@login_required
def leave_delete(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    if request.method == 'POST':
        leave.delete()
        messages.success(request, 'Leave request deleted.')
        return redirect('leave_list')
    return render(request, 'base/leave_confirm_delete.html', {'leave': leave})

@login_required
def leave_approve(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    leave.status = 'A'
    leave.save()
    messages.success(request, f'Leave request for {leave.employee} has been approved.')
    return redirect('leave_list')

@login_required
def leave_reject(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    leave.status = 'R'
    leave.save()
    messages.warning(request, f'Leave request for {leave.employee} has been rejected.')
    return redirect('leave_list')
