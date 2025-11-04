from django.contrib import admin
from django import forms
from .models import Category, BlogPost, CodeSnippet, InteractiveMap, Comment
from .widgets import CodeEditorWidget


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'color']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


class CodeSnippetForm(forms.ModelForm):
    class Meta:
        model = CodeSnippet
        fields = '__all__'
        widgets = {
            'code': CodeEditorWidget(attrs={'rows': 15}),
        }


class CodeSnippetInline(admin.StackedInline):
    model = CodeSnippet
    form = CodeSnippetForm
    extra = 0
    fields = ['title', 'language', 'code', 'description', 'order']


class InteractiveMapInline(admin.StackedInline):
    model = InteractiveMap
    extra = 0
    fields = ['title', 'description', 'center_latitude', 'center_longitude', 'zoom_level', 'geojson_data', 'order']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'featured', 'views_count', 'published_at', 'created_at']
    list_filter = ['status', 'featured', 'category', 'created_at', 'published_at']
    search_fields = ['title', 'subtitle', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-created_at']
    list_editable = ['status', 'featured']
    date_hierarchy = 'published_at'
    inlines = [InteractiveMapInline]  # Removed CodeSnippetInline - use CKEditor's built-in code snippet instead
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'subtitle', 'content', 'excerpt'),
            'description': '<strong>💡 To add code snippets:</strong> Click the <strong>"Insert/Edit code sample"</strong> button in the toolbar. You can add code anywhere in your text - between paragraphs, after sentences, etc.!'
        }),
        ('Media', {
            'fields': ('featured_image', 'featured_video_url')
        }),
        ('Organization', {
            'fields': ('category', 'tags', 'status', 'featured')
        }),
        ('Metadata', {
            'fields': ('reading_time', 'views_count', 'meta_description', 'meta_keywords')
        }),
        ('Dates', {
            'fields': ('published_at',)
        }),
    )
    
    readonly_fields = ['views_count']
    
    def save_model(self, request, obj, form, change):
        if obj.status == 'PUBLISHED' and not obj.published_at:
            from django.utils import timezone
            obj.published_at = timezone.now()
        super().save_model(request, obj, form, change)


@admin.register(CodeSnippet)
class CodeSnippetAdmin(admin.ModelAdmin):
    form = CodeSnippetForm
    list_display = ['title', 'post', 'language', 'order']
    list_filter = ['language', 'post']
    search_fields = ['title', 'code', 'description']
    
    fieldsets = (
        ('Code Information', {
            'fields': ('post', 'title', 'language', 'description')
        }),
        ('Code Editor', {
            'fields': ('code',),
            'description': 'Use Tab for indentation, Shift+Tab to unindent. Auto-indents after colons.'
        }),
        ('Display', {
            'fields': ('order',)
        }),
    )


@admin.register(InteractiveMap)
class InteractiveMapAdmin(admin.ModelAdmin):
    list_display = ['title', 'post', 'center_latitude', 'center_longitude', 'zoom_level']
    list_filter = ['post']
    search_fields = ['title', 'description']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['name', 'email', 'content']
    list_editable = ['is_approved']
    ordering = ['-created_at']
