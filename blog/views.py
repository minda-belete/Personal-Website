from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib import messages
from .models import BlogPost, Category, Comment
from taggit.models import Tag


class BlogListView(ListView):
    """List all published blog posts"""
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = BlogPost.objects.filter(status='PUBLISHED')
        
        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by tag
        tag_slug = self.request.GET.get('tag')
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        
        # Search
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(excerpt__icontains=search_query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['popular_tags'] = Tag.objects.all()[:10]
        context['featured_posts'] = BlogPost.objects.filter(status='PUBLISHED', featured=True)[:3]
        return context


class BlogDetailView(DetailView):
    """Individual blog post detail"""
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return BlogPost.objects.filter(status='PUBLISHED')
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Increment view count
        obj.increment_views()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # Get related posts by tags
        post_tags_ids = post.tags.values_list('id', flat=True)
        related_posts = BlogPost.objects.filter(
            status='PUBLISHED',
            tags__in=post_tags_ids
        ).exclude(id=post.id).distinct()[:3]
        
        context['related_posts'] = related_posts
        context['comments'] = post.comments.filter(is_approved=True)
        context['code_snippets'] = post.code_snippets.all()
        context['maps'] = post.maps.all()
        return context


def blog_category(request, slug):
    """Blog posts filtered by category"""
    category = get_object_or_404(Category, slug=slug)
    posts = BlogPost.objects.filter(status='PUBLISHED', category=category)
    
    context = {
        'category': category,
        'posts': posts,
        'categories': Category.objects.all(),
    }
    return render(request, 'blog/blog_category.html', context)


def blog_tag(request, slug):
    """Blog posts filtered by tag"""
    tag = get_object_or_404(Tag, slug=slug)
    posts = BlogPost.objects.filter(status='PUBLISHED', tags__slug=slug)
    
    context = {
        'tag': tag,
        'posts': posts,
        'categories': Category.objects.all(),
    }
    return render(request, 'blog/blog_tag.html', context)


def add_comment(request, slug):
    """Add a comment to a blog post"""
    post = get_object_or_404(BlogPost, slug=slug, status='PUBLISHED')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        website = request.POST.get('website', '')
        content = request.POST.get('content')
        
        if name and email and content:
            Comment.objects.create(
                post=post,
                name=name,
                email=email,
                website=website,
                content=content,
                is_approved=False  # Requires moderation
            )
            messages.success(request, 'Your comment has been submitted and is awaiting moderation.')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return redirect('blog:post_detail', slug=slug)
