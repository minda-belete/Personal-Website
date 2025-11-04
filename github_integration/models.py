from django.db import models
from django.utils import timezone

class GitHubRepository(models.Model):
    """GitHub repository information fetched from API"""
    # Repository identifiers
    github_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    full_name = models.CharField(max_length=300)
    
    # Repository details
    description = models.TextField(blank=True, null=True)
    url = models.URLField()
    homepage = models.URLField(blank=True, null=True)
    
    # Statistics
    stars_count = models.IntegerField(default=0)
    forks_count = models.IntegerField(default=0)
    watchers_count = models.IntegerField(default=0)
    open_issues_count = models.IntegerField(default=0)
    size = models.IntegerField(default=0, help_text="Size in KB")
    
    # Language and topics
    primary_language = models.CharField(max_length=50, blank=True, null=True)
    topics = models.JSONField(default=list, blank=True)
    
    # Status
    is_fork = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    
    # Dates
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    pushed_at = models.DateTimeField(null=True, blank=True)
    
    # Display settings
    featured = models.BooleanField(default=False, help_text="Show on homepage")
    display_order = models.IntegerField(default=0)
    custom_description = models.TextField(blank=True, help_text="Override GitHub description")
    
    # Cache
    last_synced = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-featured', 'display_order', '-stars_count']
        verbose_name = "GitHub Repository"
        verbose_name_plural = "GitHub Repositories"
    
    def __str__(self):
        return self.full_name
    
    @property
    def display_description(self):
        return self.custom_description or self.description or "No description available"

class GitHubLanguage(models.Model):
    """Programming languages used in repositories"""
    repository = models.ForeignKey(GitHubRepository, on_delete=models.CASCADE, related_name='languages')
    name = models.CharField(max_length=50)
    bytes_count = models.IntegerField(default=0)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    
    class Meta:
        ordering = ['-bytes_count']
    
    def __str__(self):
        return f"{self.name} ({self.percentage}%)"

class GitHubCommit(models.Model):
    """Recent commits for featured repositories"""
    repository = models.ForeignKey(GitHubRepository, on_delete=models.CASCADE, related_name='commits')
    sha = models.CharField(max_length=40, unique=True)
    message = models.TextField()
    author_name = models.CharField(max_length=200)
    author_email = models.EmailField()
    committed_at = models.DateTimeField()
    url = models.URLField()
    
    class Meta:
        ordering = ['-committed_at']
    
    def __str__(self):
        return f"{self.sha[:7]} - {self.message[:50]}"
