from django.contrib import admin
from .models import GitHubRepository, GitHubLanguage, GitHubCommit
from .services import GitHubService


class GitHubLanguageInline(admin.TabularInline):
    model = GitHubLanguage
    extra = 0
    readonly_fields = ['name', 'bytes_count', 'percentage']


@admin.register(GitHubRepository)
class GitHubRepositoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'primary_language', 'stars_count', 'forks_count', 'featured', 'last_synced']
    list_filter = ['primary_language', 'featured', 'is_fork', 'is_archived']
    search_fields = ['name', 'description', 'full_name']
    ordering = ['-stars_count']
    list_editable = ['featured']
    readonly_fields = ['github_id', 'full_name', 'url', 'stars_count', 'forks_count', 
                      'watchers_count', 'open_issues_count', 'size', 'primary_language',
                      'topics', 'is_fork', 'is_private', 'is_archived', 'created_at',
                      'updated_at', 'pushed_at', 'last_synced']
    inlines = [GitHubLanguageInline]
    
    fieldsets = (
        ('Repository Info', {
            'fields': ('name', 'full_name', 'description', 'custom_description', 'url', 'homepage')
        }),
        ('Statistics', {
            'fields': ('stars_count', 'forks_count', 'watchers_count', 'open_issues_count', 'size')
        }),
        ('Technical Details', {
            'fields': ('primary_language', 'topics')
        }),
        ('Status', {
            'fields': ('is_fork', 'is_private', 'is_archived')
        }),
        ('Display Settings', {
            'fields': ('featured', 'display_order')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at', 'pushed_at', 'last_synced')
        }),
    )
    
    actions = ['sync_repositories']
    
    def sync_repositories(self, request, queryset):
        """Sync selected repositories from GitHub"""
        service = GitHubService()
        count = 0
        for repo in queryset:
            service.fetch_repository_details(repo.name, sync_to_db=True)
            count += 1
        self.message_user(request, f"Successfully synced {count} repositories from GitHub.")
    sync_repositories.short_description = "Sync selected repositories from GitHub"


@admin.register(GitHubLanguage)
class GitHubLanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'repository', 'percentage', 'bytes_count']
    list_filter = ['name']
    search_fields = ['name', 'repository__name']


@admin.register(GitHubCommit)
class GitHubCommitAdmin(admin.ModelAdmin):
    list_display = ['sha', 'repository', 'author_name', 'committed_at']
    list_filter = ['repository', 'committed_at']
    search_fields = ['sha', 'message', 'author_name']
    readonly_fields = ['sha', 'message', 'author_name', 'author_email', 'committed_at', 'url']
