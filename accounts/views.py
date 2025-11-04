from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .models import User, SiteSettings, UserActivity
from .forms import UserProfileForm, UserCreationFormCustom


def log_activity(user, action, description, request):
    """Helper function to log user activities"""
    UserActivity.objects.create(
        user=user,
        action=action,
        description=description,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )


@login_required
def profile_view(request):
    """User profile page"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            log_activity(request.user, 'update', 'Updated profile information', request)
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def change_password(request):
    """Change password page"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            log_activity(request.user, 'update', 'Changed password', request)
            messages.success(request, 'Password changed successfully!')
            return redirect('accounts:profile')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'accounts/change_password.html', {'form': form})


def is_admin(user):
    """Check if user is admin"""
    return user.is_authenticated and user.role == 'admin'


@user_passes_test(is_admin)
def user_management(request):
    """User management page for admins"""
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'accounts/user_management.html', {'users': users})


@user_passes_test(is_admin)
def create_user(request):
    """Create new user"""
    if request.method == 'POST':
        form = UserCreationFormCustom(request.POST)
        if form.is_valid():
            user = form.save()
            log_activity(request.user, 'create', f'Created new user: {user.username}', request)
            messages.success(request, f'User {user.username} created successfully!')
            return redirect('accounts:user_management')
    else:
        form = UserCreationFormCustom()
    
    return render(request, 'accounts/create_user.html', {'form': form})


@user_passes_test(is_admin)
def edit_user(request, user_id):
    """Edit existing user"""
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            log_activity(request.user, 'update', f'Updated user: {user.username}', request)
            messages.success(request, f'User {user.username} updated successfully!')
            return redirect('accounts:user_management')
    else:
        form = UserProfileForm(instance=user)
    
    return render(request, 'accounts/edit_user.html', {'form': form, 'user_obj': user})


@user_passes_test(is_admin)
def delete_user(request, user_id):
    """Delete user"""
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        username = user.username
        log_activity(request.user, 'delete', f'Deleted user: {username}', request)
        user.delete()
        messages.success(request, f'User {username} deleted successfully!')
        return redirect('accounts:user_management')
    
    return render(request, 'accounts/delete_user.html', {'user_obj': user})


@user_passes_test(is_admin)
def activity_log(request):
    """View user activity log"""
    activities = UserActivity.objects.all()[:100]
    return render(request, 'accounts/activity_log.html', {'activities': activities})


@user_passes_test(is_admin)
def site_settings_view(request):
    """Site settings management"""
    settings = SiteSettings.load()
    return render(request, 'accounts/site_settings.html', {'settings': settings})
