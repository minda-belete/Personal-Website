from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extended User model with roles and additional fields"""
    
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('editor', 'Content Editor'),
        ('author', 'Author'),
        ('viewer', 'Viewer'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
    bio = models.TextField(blank=True, help_text="Short biography")
    profile_picture = models.ImageField(upload_to='user_profiles/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    
    # Permissions
    can_publish_blog = models.BooleanField(default=False, help_text="Can publish blog posts")
    can_edit_portfolio = models.BooleanField(default=False, help_text="Can edit portfolio content")
    can_manage_users = models.BooleanField(default=False, help_text="Can manage other users")
    can_view_analytics = models.BooleanField(default=False, help_text="Can view site analytics")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    
    class Meta:
        ordering = ['-date_joined']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def save(self, *args, **kwargs):
        # Auto-assign permissions based on role
        if self.role == 'admin':
            self.is_staff = True
            self.is_superuser = True
            self.can_publish_blog = True
            self.can_edit_portfolio = True
            self.can_manage_users = True
            self.can_view_analytics = True
        elif self.role == 'editor':
            self.is_staff = True
            self.can_publish_blog = True
            self.can_edit_portfolio = True
        elif self.role == 'author':
            self.is_staff = True
            self.can_publish_blog = True
        elif self.role == 'viewer':
            self.is_staff = False
            self.can_publish_blog = False
            self.can_edit_portfolio = False
            self.can_manage_users = False
            self.can_view_analytics = False
        
        super().save(*args, **kwargs)


class SiteSettings(models.Model):
    """Global site settings"""
    
    # Site Information
    site_name = models.CharField(max_length=100, default="My Portfolio")
    site_tagline = models.CharField(max_length=200, blank=True)
    site_description = models.TextField(blank=True)
    site_logo = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site/', blank=True, null=True)
    
    # Contact Information
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_address = models.TextField(blank=True)
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    
    # SEO Settings
    meta_keywords = models.TextField(blank=True, help_text="Comma-separated keywords")
    google_analytics_id = models.CharField(max_length=50, blank=True)
    google_site_verification = models.CharField(max_length=100, blank=True)
    
    # Features
    enable_blog = models.BooleanField(default=True)
    enable_comments = models.BooleanField(default=True)
    enable_github_integration = models.BooleanField(default=True)
    maintenance_mode = models.BooleanField(default=False)
    
    # Email Settings
    email_notifications = models.BooleanField(default=True)
    admin_email = models.EmailField(blank=True)
    
    # Security
    require_email_verification = models.BooleanField(default=False)
    max_login_attempts = models.IntegerField(default=5)
    session_timeout_minutes = models.IntegerField(default=60)
    
    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'
    
    def __str__(self):
        return f"Site Settings - {self.site_name}"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        """Load the singleton instance"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class UserActivity(models.Model):
    """Track user activities for audit trail"""
    
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('view', 'View'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'
    
    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"
