from django.contrib import admin
from django.shortcuts import redirect
from .models import HomePage, Profile, Education, Research, Skill, Experience, TimelineEntry, ResearchPageSettings, AboutPageSettings, IndustryIndexSettings, IndustryRanking


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Hero Section', {
            'fields': ('hero_title', 'hero_description', 'hero_image'),
            'description': 'Main landing page hero section content'
        }),
        ('CV Upload', {
            'fields': ('cv_file',),
            'description': 'Upload your CV in PDF format'
        }),
        ('Call to Action Button', {
            'fields': ('cta_primary_text',),
            'description': 'Customize the CV button text'
        }),
        ('About Section', {
            'fields': ('about_title', 'about_content'),
            'classes': ('collapse',)
        }),
        ('Stats/Highlights', {
            'fields': ('show_stats', 'stat1_number', 'stat1_label', 'stat2_number', 'stat2_label', 'stat3_number', 'stat3_label'),
            'classes': ('collapse',)
        }),
        ('Social Links', {
            'fields': ('github_url', 'linkedin_url', 'twitter_url', 'email'),
            'classes': ('collapse',)
        }),
        ('Page Settings', {
            'fields': ('show_recent_blog', 'show_featured_repos', 'show_skills'),
            'description': 'Control which sections appear on the homepage'
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one HomePage instance
        return not HomePage.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False


@admin.register(Research)
class ResearchAdmin(admin.ModelAdmin):
    list_display = ['title', 'research_type', 'publication_venue', 'publication_date', 'featured', 'order']
    list_filter = ['research_type', 'featured', 'publication_date']
    search_fields = ['title', 'authors', 'abstract', 'tags']
    ordering = ['order', '-publication_date']
    list_editable = ['featured', 'order']
    
    change_list_template = 'admin/portfolio/research_changelist.html'
    
    fieldsets = (
        ('Required Information', {
            'fields': ('title', 'research_type', 'authors'),
            'description': 'These fields are required.'
        }),
        ('Optional Details', {
            'fields': ('abstract', 'publication_venue', 'publication_date', 'doi', 'url'),
            'description': 'All fields in this section are optional.',
            'classes': ('collapse',)
        }),
        ('Media (Optional)', {
            'fields': ('pdf_file', 'thumbnail'),
            'classes': ('collapse',)
        }),
        ('Organization', {
            'fields': ('tags', 'featured', 'order')
        }),
    )
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        # Handle page settings form submission
        if request.method == 'POST' and 'save_page_settings' in request.POST:
            settings, created = ResearchPageSettings.objects.get_or_create(pk=1)
            settings.page_title = request.POST.get('page_title', settings.page_title)
            settings.page_description = request.POST.get('page_description', settings.page_description)
            settings.all_research_heading = request.POST.get('all_research_heading', settings.all_research_heading)
            settings.save()
            self.message_user(request, 'Research page settings updated successfully.')
            return redirect('admin:portfolio_research_changelist')
        
        # Get or create page settings
        settings, created = ResearchPageSettings.objects.get_or_create(
            pk=1,
            defaults={
                'page_title': 'Research & Publications',
                'page_description': 'Explore my research contributions, publications, and academic work.',
                'all_research_heading': 'All Publications'
            }
        )
        extra_context['research_page_settings'] = settings
        
        return super().changelist_view(request, extra_context=extra_context)
    
    # Make it easier to see what's required
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Add help text to show required vs optional
        if 'title' in form.base_fields:
            form.base_fields['title'].help_text = '✱ Required'
        if 'research_type' in form.base_fields:
            form.base_fields['research_type'].help_text = '✱ Required'
        if 'authors' in form.base_fields:
            form.base_fields['authors'].help_text = '✱ Required - Comma-separated list'
        return form


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'order']
    list_filter = ['category']
    search_fields = ['name']
    ordering = ['category', 'order']
    list_editable = ['proficiency', 'order']
    
    change_list_template = 'admin/portfolio/skill_changelist.html'
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        # Handle bulk add form submission
        if request.method == 'POST' and 'bulk_add' in request.POST:
            category = request.POST.get('bulk_category')
            skills_text = request.POST.get('bulk_skills_text', '')
            
            if category and skills_text:
                max_order = Skill.objects.filter(category=category).count()
                count = 0
                
                for idx, line in enumerate(skills_text.strip().split('\n')):
                    line = line.strip()
                    if not line:
                        continue
                    
                    parts = line.split('|')
                    name = parts[0].strip()
                    proficiency = int(parts[1].strip()) if len(parts) > 1 else 50
                    icon = parts[2].strip() if len(parts) > 2 else ''
                    subcategory = parts[3].strip().upper() if len(parts) > 3 else 'OTHER'
                    
                    # Update or create - replace if exists with same name
                    skill, created = Skill.objects.update_or_create(
                        name=name,
                        defaults={
                            'category': category,
                            'proficiency': proficiency,
                            'icon': icon,
                            'subcategory': subcategory,
                            'order': max_order + idx
                        }
                    )
                    count += 1
                
                self.message_user(request, f'Successfully added {count} skills to {dict(Skill.SKILL_CATEGORY_CHOICES)[category]} category.')
                return redirect('admin:portfolio_skill_changelist')
        
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'start_date', 'end_date', 'is_current', 'order']
    list_filter = ['company']
    search_fields = ['title', 'company', 'description']
    ordering = ['order', '-start_date']
    list_editable = ['order']
    
    fieldsets = (
        ('Required Information', {
            'fields': ('title', 'company', 'start_date', 'description'),
            'description': 'These fields are required.'
        }),
        ('Optional Details', {
            'fields': ('end_date', 'location', 'achievements', 'company_logo'),
            'description': 'All fields in this section are optional. Leave end_date blank for current positions.',
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('order',)
        }),
    )


@admin.register(TimelineEntry)
class TimelineEntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'period', 'year', 'is_active', 'order']
    list_filter = ['period', 'is_active', 'year']
    search_fields = ['title', 'content']
    ordering = ['period', 'year', 'order']
    list_editable = ['order', 'is_active']
    
    change_list_template = 'admin/portfolio/about_changelist.html'
    
    fieldsets = (
        ('Timeline Information', {
            'fields': ('period', 'year', 'title'),
            'description': 'Basic information about this timeline entry'
        }),
        ('Content', {
            'fields': ('content', 'image'),
            'description': 'The story and optional image for this period'
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active'),
            'description': 'Control visibility and order of this entry'
        }),
    )
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        # Handle about page settings form submission
        if request.method == 'POST' and 'save_about_settings' in request.POST:
            settings, created = AboutPageSettings.objects.get_or_create(pk=1)
            settings.intro_bio = request.POST.get('intro_bio', settings.intro_bio)
            settings.github_url = request.POST.get('github_url', settings.github_url)
            settings.linkedin_url = request.POST.get('linkedin_url', settings.linkedin_url)
            settings.twitter_url = request.POST.get('twitter_url', settings.twitter_url)
            settings.google_scholar_url = request.POST.get('google_scholar_url', settings.google_scholar_url)
            settings.orcid_url = request.POST.get('orcid_url', settings.orcid_url)
            
            # Handle file uploads
            if 'profile_image' in request.FILES:
                settings.profile_image = request.FILES['profile_image']
            if 'cv_file' in request.FILES:
                settings.cv_file = request.FILES['cv_file']
            
            settings.save()
            self.message_user(request, 'About page settings updated successfully.')
            return redirect('admin:portfolio_timelineentry_changelist')
        
        # Get or create about page settings
        settings, created = AboutPageSettings.objects.get_or_create(
            pk=1,
            defaults={'intro_bio': ''}
        )
        extra_context['about_page_settings'] = settings
        
        return super().changelist_view(request, extra_context=extra_context)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Add helpful text
        if 'period' in form.base_fields:
            form.base_fields['period'].help_text = 'Choose whether this is about your past, present, or future'
        if 'year' in form.base_fields:
            form.base_fields['year'].help_text = 'The year this entry represents (e.g., 2013, 2022, 2030, 2050)'
        if 'title' in form.base_fields:
            form.base_fields['title'].help_text = 'e.g., "Me as a Kid", "Me in 2022", "Me in 2050"'
        return form


@admin.register(IndustryIndexSettings)
class IndustryIndexSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Page Content', {
            'fields': ('page_description', 'current_industry'),
            'description': 'Customize the Industry Index page description and current industry'
        }),
        ('AI Configuration', {
            'fields': ('openai_api_key', 'last_generated'),
            'description': 'OpenAI API settings for generating rankings'
        }),
    )
    
    readonly_fields = ['last_generated']
    
    def has_add_permission(self, request):
        return not IndustryIndexSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(IndustryRanking)
class IndustryRankingAdmin(admin.ModelAdmin):
    list_display = ['rank', 'industry_name', 'relevance_score', 'is_current_industry', 'is_active', 'updated_at']
    list_filter = ['is_current_industry', 'is_active']
    search_fields = ['industry_name', 'reasoning', 'key_skills']
    ordering = ['rank']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Industry Information', {
            'fields': ('industry_name', 'rank', 'relevance_score'),
        }),
        ('AI Analysis', {
            'fields': ('reasoning', 'key_skills'),
        }),
        ('Settings', {
            'fields': ('is_current_industry', 'is_active'),
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow AI to create rankings
        return False
