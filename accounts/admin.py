from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.html import format_html
from .models import User, SiteSettings, UserActivity


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    
    list_display = ('username', 'email', 'role_badge', 'full_name', 'is_active', 'last_login', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        ('Login Credentials', {
            'fields': ('username', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'bio', 'profile_picture', 'website')
        }),
        ('Role & Permissions', {
            'fields': ('role', 'can_publish_blog', 'can_edit_portfolio', 'can_manage_users', 'can_view_analytics'),
            'description': 'Role automatically sets permissions. You can override individual permissions if needed.'
        }),
        ('System Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined', 'last_login_ip'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        ('Create New User', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'first_name', 'last_name'),
        }),
    )
    
    def role_badge(self, obj):
        colors = {
            'admin': '#dc3545',
            'editor': '#0d6efd',
            'author': '#198754',
            'viewer': '#6c757d',
        }
        color = colors.get(obj.role, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_role_display()
        )
    role_badge.short_description = 'Role'
    
    def full_name(self, obj):
        return obj.get_full_name() or '-'
    full_name.short_description = 'Full Name'
    
    actions = ['activate_users', 'deactivate_users', 'make_editor', 'make_author']
    
    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} users activated successfully.")
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} users deactivated successfully.")
    deactivate_users.short_description = "Deactivate selected users"
    
    def make_editor(self, request, queryset):
        queryset.update(role='editor')
        self.message_user(request, f"{queryset.count()} users changed to Editor role.")
    make_editor.short_description = "Change role to Editor"
    
    def make_author(self, request, queryset):
        queryset.update(role='author')
        self.message_user(request, f"{queryset.count()} users changed to Author role.")
    make_author.short_description = "Change role to Author"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Site Information', {
            'fields': ('site_name', 'site_tagline', 'site_description', 'site_logo', 'favicon'),
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone', 'contact_address'),
        }),
        ('Social Media Links', {
            'fields': ('facebook_url', 'twitter_url', 'linkedin_url', 'github_url', 'instagram_url'),
            'classes': ('collapse',)
        }),
        ('SEO Settings', {
            'fields': ('meta_keywords', 'google_analytics_id', 'google_site_verification'),
            'classes': ('collapse',)
        }),
        ('Feature Toggles', {
            'fields': ('enable_blog', 'enable_comments', 'enable_github_integration', 'maintenance_mode'),
        }),
        ('Email Configuration', {
            'fields': ('email_notifications', 'admin_email'),
            'classes': ('collapse',)
        }),
        ('Security Settings', {
            'fields': ('require_email_verification', 'max_login_attempts', 'session_timeout_minutes'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion
        return False
    
    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'description_short', 'ip_address', 'timestamp')
    list_filter = ('action', 'timestamp', 'user')
    search_fields = ('user__username', 'description', 'ip_address')
    readonly_fields = ('user', 'action', 'description', 'ip_address', 'user_agent', 'timestamp')
    date_hierarchy = 'timestamp'
    
    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
