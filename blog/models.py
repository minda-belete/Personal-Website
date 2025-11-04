from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from tinymce.models import HTMLField
from taggit.managers import TaggableManager

class Category(models.Model):
    """Blog post categories"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    color = models.CharField(max_length=7, default="#3498db", help_text="Hex color code")
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class BlogPost(models.Model):
    """Advanced blog post model with rich media support"""
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PUBLISHED', 'Published'),
        ('ARCHIVED', 'Archived'),
    ]
    
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    subtitle = models.CharField(max_length=300, blank=True)
    
    # Rich content with TinyMCE
    content = HTMLField(
        help_text="Main blog content with support for images, videos, GIFs, code, and more"
    )
    excerpt = models.TextField(blank=True, help_text="Short summary for previews")
    
    # Media
    featured_image = models.ImageField(upload_to='blog/featured/', blank=True, null=True)
    featured_video_url = models.URLField(blank=True, help_text="YouTube, Vimeo, etc.")
    
    # Organization
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    tags = TaggableManager(blank=True)
    
    # Metadata
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    featured = models.BooleanField(default=False, help_text="Display on homepage")
    views_count = models.IntegerField(default=0)
    reading_time = models.IntegerField(default=5, help_text="Estimated reading time in minutes")
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        # Auto-generate excerpt if not provided
        if not self.excerpt and self.content:
            # Strip HTML and take first 200 characters
            import re
            text = re.sub('<[^<]+?>', '', self.content)
            self.excerpt = text[:200] + '...' if len(text) > 200 else text
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])

class CodeSnippet(models.Model):
    """Standalone code snippets for blog posts"""
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('java', 'Java'),
        ('cpp', 'C++'),
        ('csharp', 'C#'),
        ('php', 'PHP'),
        ('ruby', 'Ruby'),
        ('go', 'Go'),
        ('rust', 'Rust'),
        ('sql', 'SQL'),
        ('html', 'HTML'),
        ('css', 'CSS'),
        ('bash', 'Bash'),
        ('r', 'R'),
        ('matlab', 'MATLAB'),
        ('other', 'Other'),
    ]
    
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='code_snippets')
    title = models.CharField(max_length=200, blank=True)
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='python')
    code = models.TextField()
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.title or 'Code Snippet'} ({self.language})"

class InteractiveMap(models.Model):
    """Interactive maps for blog posts"""
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='maps')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Map configuration
    center_latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    center_longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    zoom_level = models.IntegerField(default=10)
    
    # GeoJSON data or external URL
    geojson_data = models.TextField(blank=True, help_text="GeoJSON data for map features")
    external_url = models.URLField(blank=True, help_text="Link to external map service")
    
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    """Blog post comments"""
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField(blank=True)
    content = models.TextField()
    
    # Moderation
    is_approved = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"
