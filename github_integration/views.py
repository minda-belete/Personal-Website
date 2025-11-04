from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import GitHubRepository
from .services import GitHubService


class RepositoryListView(ListView):
    """List all GitHub repositories"""
    model = GitHubRepository
    template_name = 'github_integration/repository_list.html'
    context_object_name = 'repositories'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = GitHubRepository.objects.filter(is_archived=False)
        
        # Filter by language
        language = self.request.GET.get('language')
        if language:
            queryset = queryset.filter(primary_language=language)
        
        # Sort options
        sort = self.request.GET.get('sort', '-stars_count')
        if sort in ['-stars_count', '-forks_count', '-updated_at', 'name']:
            queryset = queryset.order_by(sort)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['languages'] = GitHubRepository.objects.values_list(
            'primary_language', flat=True
        ).distinct().exclude(primary_language__isnull=True)
        context['featured_repos'] = GitHubRepository.objects.filter(featured=True)[:6]
        return context


class RepositoryDetailView(DetailView):
    """Individual repository detail"""
    model = GitHubRepository
    template_name = 'github_integration/repository_detail.html'
    context_object_name = 'repository'
    slug_field = 'name'
    slug_url_kwarg = 'name'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        repo = self.get_object()
        context['languages'] = repo.languages.all()
        context['recent_commits'] = repo.commits.all()[:10]
        return context


@staff_member_required
def sync_repositories(request):
    """Sync all repositories from GitHub (admin only)"""
    try:
        service = GitHubService()
        repos = service.sync_all_data()
        messages.success(request, f'Successfully synced {len(repos)} repositories from GitHub!')
    except Exception as e:
        messages.error(request, f'Error syncing repositories: {str(e)}')
    
    from django.shortcuts import redirect
    return redirect('github:repository_list')
