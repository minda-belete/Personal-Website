from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, Http404
from django.views.generic import ListView, DetailView
from django.template.response import TemplateResponse
from .models import Profile, Education, Research, Skill, Experience, HomePage
from blog.models import BlogPost
from github_integration.models import GitHubRepository


def home(request):
    """Homepage view with editable content"""
    # Get or create homepage content
    homepage, created = HomePage.objects.get_or_create(
        pk=1,
        defaults={
            'hero_title': 'Your Name',
            'hero_description': 'Research Assistant at New York University Abu Dhabi, MSc student at Georgia Institute of Technology'
        }
    )
    
    try:
        profile = Profile.objects.first()
    except Profile.DoesNotExist:
        profile = None
    
    education = Education.objects.all()[:3]
    research = Research.objects.filter(featured=True)[:3]
    skills = Skill.objects.all()[:6]
    experience = Experience.objects.all()[:3]
    
    # Get recent blog posts if enabled
    recent_posts = []
    if homepage.show_recent_blog:
        recent_posts = BlogPost.objects.filter(status='PUBLISHED').order_by('-published_at')[:3]
    
    # Get featured GitHub repos if enabled
    featured_repos = []
    if homepage.show_featured_repos:
        featured_repos = GitHubRepository.objects.filter(featured=True)[:6]
    
    context = {
        'homepage': homepage,
        'profile': profile,
        'education': education,
        'research': research,
        'skills': skills if homepage.show_skills else [],
        'experience': experience,
        'recent_posts': recent_posts,
        'featured_repos': featured_repos,
    }
    return render(request, 'portfolio/home.html', context)


def about(request):
    """About page with profile information and timeline"""
    from .models import TimelineEntry, AboutPageSettings
    
    # Get about page settings
    about_settings, created = AboutPageSettings.objects.get_or_create(
        pk=1,
        defaults={'intro_bio': ''}
    )
    
    # Get timeline entries grouped by period
    past_entries = TimelineEntry.objects.filter(period='PAST', is_active=True).order_by('year', 'order')
    present_entries = TimelineEntry.objects.filter(period='PRESENT', is_active=True).order_by('year', 'order')
    future_entries = TimelineEntry.objects.filter(period='FUTURE', is_active=True).order_by('year', 'order')
    
    context = {
        'about_settings': about_settings,
        'past_entries': past_entries,
        'present_entries': present_entries,
        'future_entries': future_entries,
    }
    return render(request, 'portfolio/about.html', context)


def skills_view(request):
    """Skills page with filtering"""
    all_skills = Skill.objects.all()
    
    # Count by category
    hard_count = all_skills.filter(category='HARD').count()
    soft_count = all_skills.filter(category='SOFT').count()
    hobbies_count = all_skills.filter(category='HOBBIES').count()
    
    # Get unique subcategories that exist in database
    from django.db.models import Count
    subcategory_data = []
    subcategories = all_skills.exclude(subcategory='OTHER').values('subcategory').annotate(
        count=Count('id')
    ).order_by('subcategory')
    
    for subcat in subcategories:
        if subcat['subcategory']:
            # Get display name
            display_name = dict(Skill.SUBCATEGORY_CHOICES).get(
                subcat['subcategory'], 
                subcat['subcategory'].replace('_', ' ').title()
            )
            subcategory_data.append({
                'value': subcat['subcategory'],
                'display': display_name,
                'count': subcat['count']
            })
    
    context = {
        'all_skills': all_skills,
        'hard_count': hard_count,
        'soft_count': soft_count,
        'hobbies_count': hobbies_count,
        'subcategories': subcategory_data,
    }
    return render(request, 'portfolio/skills.html', context)


def research_view(request):
    """Research and publications page"""
    from .models import ResearchPageSettings
    
    research = Research.objects.all()
    featured_research = research.filter(featured=True)
    
    # Get or create research page settings
    research_settings, created = ResearchPageSettings.objects.get_or_create(
        pk=1,
        defaults={
            'page_title': 'Research & Publications',
            'page_description': 'Explore my research contributions, publications, and academic work.',
            'all_research_heading': 'All Publications'
        }
    )
    
    context = {
        'research': research,
        'featured_research': featured_research,
        'research_settings': research_settings,
    }
    return render(request, 'portfolio/research.html', context)


def research_detail(request, pk):
    """Individual research project detail"""
    research = get_object_or_404(Research, pk=pk)
    context = {'research': research}
    return render(request, 'portfolio/research_detail.html', context)


def experience_view(request):
    """Work experience page"""
    experience = Experience.objects.all()
    context = {'experience': experience}
    return render(request, 'portfolio/experience.html', context)


def download_cv(request):
    """Download CV PDF file"""
    from .models import AboutPageSettings
    try:
        about_settings = AboutPageSettings.objects.first()
        if about_settings and about_settings.cv_file:
            return FileResponse(about_settings.cv_file.open('rb'), as_attachment=True, filename='CV.pdf')
    except AboutPageSettings.DoesNotExist:
        pass
    raise Http404("CV file not found")


def sitemap(request):
    """Generate sitemap.xml for SEO"""
    blog_posts = BlogPost.objects.filter(status='PUBLISHED').order_by('-published_at')
    return TemplateResponse(request, 'sitemap.xml', {
        'blog_posts': blog_posts,
    }, content_type='application/xml')


def industry_index(request):
    """Industry Index page with AI-generated rankings"""
    from .models import IndustryIndexSettings, IndustryRanking
    from .industry_analyzer import update_industry_rankings
    from django.contrib import messages
    
    # Get or create settings
    settings, created = IndustryIndexSettings.objects.get_or_create(
        pk=1,
        defaults={
            'page_description': 'This ranking is generated by AI analyzing my skills, research interests, blog posts, education, and professional activities. The index updates regularly to reflect my evolving expertise and interests.'
        }
    )
    
    # Handle manual refresh request
    if request.method == 'POST' and 'refresh_rankings' in request.POST:
        if settings.openai_api_key:
            success = update_industry_rankings(settings.openai_api_key)
            if success:
                messages.success(request, 'Industry rankings updated successfully!')
            else:
                messages.error(request, 'Failed to update rankings. Please check your API key.')
        else:
            messages.error(request, 'OpenAI API key not configured.')
        return redirect('portfolio:industry_index')
    
    # Get rankings
    rankings = IndustryRanking.objects.filter(is_active=True)[:10]
    top_5_rankings = rankings[:5]
    
    # Check if rankings need to be generated
    needs_generation = not rankings.exists()
    
    context = {
        'settings': settings,
        'rankings': rankings,
        'top_5_rankings': top_5_rankings,
        'needs_generation': needs_generation,
    }
    return render(request, 'portfolio/industry_index.html', context)


def robots_txt(request):
    """Generate robots.txt for SEO"""
    return TemplateResponse(request, 'robots.txt', {}, content_type='text/plain')
