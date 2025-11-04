from django.db import models
from django.core.validators import URLValidator
from tinymce.models import HTMLField

class HomePage(models.Model):
    """Editable homepage content"""
    # Hero Section
    hero_title = models.CharField(max_length=200, default="Your Name", help_text="Your full name")
    hero_description = HTMLField(default="Research Assistant at New York University Abu Dhabi, MSc student at Georgia Institute of Technology", help_text="Your professional title and brief introduction - supports rich text formatting")
    hero_image = models.ImageField(upload_to='homepage/', blank=True, null=True)
    
    # CV Upload
    cv_file = models.FileField(upload_to='cv/', blank=True, null=True, help_text="Upload your CV (PDF format)")
    
    # Call to Action Button
    cta_primary_text = models.CharField(max_length=50, default="View CV", help_text="Text for the CV button")
    
    # About Section
    about_title = models.CharField(max_length=100, default="About Me")
    about_content = models.TextField(blank=True)
    
    # Stats/Highlights
    show_stats = models.BooleanField(default=True)
    stat1_number = models.CharField(max_length=20, default="5+", blank=True)
    stat1_label = models.CharField(max_length=50, default="Years Experience", blank=True)
    stat2_number = models.CharField(max_length=20, default="10+", blank=True)
    stat2_label = models.CharField(max_length=50, default="Projects", blank=True)
    stat3_number = models.CharField(max_length=20, default="20+", blank=True)
    stat3_label = models.CharField(max_length=50, default="Skills", blank=True)
    
    # Social Links
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    
    # Settings
    show_recent_blog = models.BooleanField(default=True, help_text="Show recent blog posts section")
    show_featured_repos = models.BooleanField(default=True, help_text="Show featured GitHub repositories")
    show_skills = models.BooleanField(default=True, help_text="Show skills section")
    
    class Meta:
        verbose_name = "Homepage Content"
        verbose_name_plural = "Homepage Content"
    
    def __str__(self):
        return "Homepage Content"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and HomePage.objects.exists():
            raise ValueError('Only one HomePage instance is allowed')
        return super().save(*args, **kwargs)

class Profile(models.Model):
    """Main profile information"""
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200, help_text="e.g., PhD Student, Research Scientist")
    bio = models.TextField(help_text="Main bio/introduction")
    short_bio = HTMLField(blank=True, help_text="Short bio for About page (appears before timeline)")
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=200, blank=True)
    
    # Social links
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    google_scholar_url = models.URLField(blank=True)
    orcid_url = models.URLField(blank=True)
    
    # Profile image
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    cv_file = models.FileField(upload_to='cv/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"
    
    def __str__(self):
        return self.name

class Education(models.Model):
    """Education history"""
    DEGREE_CHOICES = [
        ('BS', 'Bachelor of Science'),
        ('BA', 'Bachelor of Arts'),
        ('MS', 'Master of Science'),
        ('MA', 'Master of Arts'),
        ('PHD', 'Doctor of Philosophy'),
        ('MBA', 'Master of Business Administration'),
        ('OTHER', 'Other'),
    ]
    
    degree = models.CharField(max_length=10, choices=DEGREE_CHOICES)
    field_of_study = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="Leave blank if currently enrolled")
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='education/', blank=True, null=True)
    order = models.IntegerField(default=0, help_text="Order of display (lower numbers first)")
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = "Education"
        verbose_name_plural = "Education"
    
    def __str__(self):
        return f"{self.degree} in {self.field_of_study} - {self.institution}"

class Research(models.Model):
    """Research projects and publications"""
    RESEARCH_TYPE_CHOICES = [
        ('PUBLICATION', 'Publication'),
        ('PROJECT', 'Research Project'),
        ('PATENT', 'Patent'),
        ('CONFERENCE', 'Conference Paper'),
    ]
    
    # Required fields
    title = models.CharField(max_length=300)
    research_type = models.CharField(max_length=20, choices=RESEARCH_TYPE_CHOICES)
    authors = models.CharField(max_length=500, help_text="Comma-separated list of authors")
    
    # Optional fields
    abstract = models.TextField(blank=True, help_text="Research abstract or description")
    publication_venue = models.CharField(max_length=300, blank=True, help_text="Journal, Conference, etc.")
    publication_date = models.DateField(null=True, blank=True, help_text="Publication date")
    doi = models.CharField(max_length=100, blank=True, help_text="Digital Object Identifier")
    url = models.URLField(blank=True, help_text="Link to paper/project")
    pdf_file = models.FileField(upload_to='research/pdfs/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='research/thumbnails/', blank=True, null=True)
    tags = models.CharField(max_length=300, blank=True, help_text="Comma-separated tags")
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-publication_date', 'order']
        verbose_name = "Research"
        verbose_name_plural = "Research"
    
    def __str__(self):
        return self.title

class Skill(models.Model):
    """Technical and professional skills"""
    SKILL_CATEGORY_CHOICES = [
        ('HARD', 'Hard Skills'),
        ('SOFT', 'Soft Skills'),
        ('HOBBIES', 'Hobbies'),
    ]
    
    SUBCATEGORY_CHOICES = [
        ('MICROECONOMICS', 'Microeconomics'),
        ('MACROECONOMICS', 'Macroeconomics'),
        ('SPATIAL_ECONOMICS', 'Spatial Economics'),
        ('ECONOMETRICS', 'Econometrics'),
        ('PROGRAMMING', 'Programming & Tools'),
        ('AI_ML', 'AI & Machine Learning'),
        ('DATA_ANALYSIS', 'Data Analysis'),
        ('GIS', 'GIS & Mapping'),
        ('COMMUNICATION', 'Communication'),
        ('LEADERSHIP', 'Leadership'),
        ('CREATIVE', 'Creative'),
        ('OTHER', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=SKILL_CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=30, choices=SUBCATEGORY_CHOICES, default='OTHER', help_text="Skill subcategory for filtering")
    proficiency = models.IntegerField(default=50, help_text="Proficiency level (0-100)")
    icon = models.CharField(max_length=100, blank=True, help_text="Font Awesome icon class")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['category', 'order']
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class Experience(models.Model):
    """Work experience"""
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="Leave blank if current position")
    description = models.TextField()
    achievements = models.TextField(blank=True, help_text="Key achievements (one per line)")
    company_logo = models.ImageField(upload_to='experience/', blank=True, null=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.title} at {self.company}"
    
    @property
    def is_current(self):
        return self.end_date is None


class ResearchPageSettings(models.Model):
    """Settings for the Research page"""
    page_title = models.CharField(max_length=200, default="Research & Publications", help_text="Main title for the research page")
    page_description = HTMLField(default="Explore my research contributions, publications, and academic work.", help_text="Description/bio that appears below the title - supports rich text formatting")
    all_research_heading = models.CharField(max_length=100, default="All Publications", help_text="Heading for the all research section (e.g., 'All Publications', 'Working Papers', 'Research Projects')")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Research Page Settings"
        verbose_name_plural = "Research Page Settings"
    
    def __str__(self):
        return "Research Page Settings"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and ResearchPageSettings.objects.exists():
            raise ValueError('Only one ResearchPageSettings instance is allowed')
        return super().save(*args, **kwargs)


class AboutPageSettings(models.Model):
    """Settings for the About Me page"""
    intro_bio = HTMLField(blank=True, help_text="Introduction bio that appears at the top of the About page, before the timeline - supports rich text formatting")
    
    # Profile image
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True, help_text="Your profile photo")
    
    # Social links
    github_url = models.URLField(blank=True, help_text="GitHub profile URL")
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn profile URL")
    twitter_url = models.URLField(blank=True, help_text="Twitter/X profile URL")
    google_scholar_url = models.URLField(blank=True, help_text="Google Scholar profile URL")
    orcid_url = models.URLField(blank=True, help_text="ORCID profile URL")
    
    # CV file
    cv_file = models.FileField(upload_to='cv/', blank=True, null=True, help_text="Upload your CV (PDF format)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "About Page Settings"
        verbose_name_plural = "About Page Settings"
    
    def __str__(self):
        return "About Page Settings"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and AboutPageSettings.objects.exists():
            raise ValueError('Only one AboutPageSettings instance is allowed')
        return super().save(*args, **kwargs)


class TimelineEntry(models.Model):
    """Timeline entries for About page - My Past, Present, and Future"""
    PERIOD_CHOICES = [
        ('PAST', 'My Past'),
        ('PRESENT', 'My Present'),
        ('FUTURE', 'My Future (Aspirations)'),
    ]
    
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES, help_text="Which main section this entry belongs to")
    year = models.IntegerField(null=True, blank=True, help_text="Year for this timeline entry (e.g., 2013, 2022, 2030) - Optional")
    title = models.CharField(max_length=200, blank=True, help_text="Title for this period (e.g., 'Me as a Kid', 'Me in 2022') - Optional")
    content = HTMLField(help_text="Content describing this period of your life - supports rich text formatting")
    image = models.ImageField(upload_to='timeline/', blank=True, null=True, help_text="Optional image for this period")
    order = models.IntegerField(default=0, help_text="Order within the period (lower numbers first)")
    is_active = models.BooleanField(default=True, help_text="Show/hide this entry")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['period', 'year', 'order']
        verbose_name = "About Me - Timeline Entry"
        verbose_name_plural = "About Me"
    
    def __str__(self):
        if self.title and self.year:
            return f"{self.get_period_display()} - {self.title} ({self.year})"
        elif self.title:
            return f"{self.get_period_display()} - {self.title}"
        elif self.year:
            return f"{self.get_period_display()} - {self.year}"
        else:
            return f"{self.get_period_display()} - Entry"
    
    def get_period_icon(self):
        """Return appropriate icon for each period"""
        icons = {
            'PAST': 'fas fa-history',
            'PRESENT': 'fas fa-clock',
            'FUTURE': 'fas fa-rocket'
        }
        return icons.get(self.period, 'fas fa-circle')


class IndustryIndexSettings(models.Model):
    """Settings for the Industry Index page"""
    page_description = HTMLField(
        default="This ranking is generated by AI analyzing my skills, research interests, blog posts, education, and professional activities. The index updates regularly to reflect my evolving expertise and interests.",
        help_text="Description explaining how the industry ranking works"
    )
    current_industry = models.CharField(
        max_length=200,
        blank=True,
        help_text="Your current industry (e.g., 'Technology', 'Finance', 'Healthcare'). Leave blank to auto-detect from homepage."
    )
    openai_api_key = models.CharField(
        max_length=500,
        blank=True,
        help_text="OpenAI API key for generating industry rankings"
    )
    last_generated = models.DateTimeField(null=True, blank=True, help_text="Last time rankings were generated")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Industry Index Settings"
        verbose_name_plural = "Industry Index Settings"
    
    def __str__(self):
        return "Industry Index Settings"
    
    def save(self, *args, **kwargs):
        if not self.pk and IndustryIndexSettings.objects.exists():
            raise ValueError('Only one IndustryIndexSettings instance is allowed')
        return super().save(*args, **kwargs)


class IndustryRanking(models.Model):
    """AI-generated industry rankings"""
    industry_name = models.CharField(max_length=200, help_text="Name of the industry")
    rank = models.IntegerField(help_text="Ranking position (1 = most relevant)")
    relevance_score = models.FloatField(help_text="Relevance score (0-100)")
    reasoning = models.TextField(help_text="AI-generated explanation for this ranking")
    key_skills = models.TextField(blank=True, help_text="Comma-separated list of relevant skills")
    
    is_current_industry = models.BooleanField(default=False, help_text="Is this your current industry?")
    is_active = models.BooleanField(default=True, help_text="Show/hide this ranking")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['rank']
        verbose_name = "Industry Ranking"
        verbose_name_plural = "Industry Rankings"
    
    def __str__(self):
        return f"#{self.rank} - {self.industry_name} ({self.relevance_score}%)"
