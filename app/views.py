import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, F
# pyrefly: ignore [missing-import]
from .models import ContactMessage, Blog


def index(request):
    """
    Renders the Neo-Brutalist developer portfolio homepage.
    """
    featured_blogs = Blog.objects.filter(is_published=True).order_by('-published_at')[:3]
    return render(request, 'index.html', {
        'featured_blogs': featured_blogs
    })


@require_POST
def contact_submit(request):
    """
    Handles contact form submissions and saves them to the ContactMessage model.
    Supports both JSON payloads (AJAX fetch) and standard form encoded POST.
    """
    name = ""
    email = ""
    subject = ""
    message = ""

    # Check content type
    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body.decode('utf-8'))
            name = data.get('name', '').strip()
            email = data.get('email', '').strip()
            subject = data.get('subject', '').strip()
            message = data.get('message', '').strip()
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON payload'}, status=400)
    else:
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

    # Validation
    if not name or not email or not message:
        return JsonResponse({
            'status': 'error',
            'message': 'Please fill out all required fields (Name, Email, Message).'
        }, status=400)

    # Save to database
    contact_obj = ContactMessage.objects.create(
        name=name,
        email=email,
        subject=subject or 'General Inquiry',
        message=message
    )

    return JsonResponse({
        'status': 'success',
        'message': f'Thank you {name}! Your transmission has been saved. Sathya will reply within 24 hours.',
        'id': contact_obj.id
    })


def blog_list(request):
    """
    Renders the official blogs listing page with search, categories, and tags.
    """
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    blogs = Blog.objects.filter(is_published=True)

    if query:
        blogs = blogs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__icontains=query)
        )

    if category and category != 'All':
        blogs = blogs.filter(category__iexact=category)

    # Collect distinct categories for tabs
    all_categories = Blog.objects.filter(is_published=True).values_list('category', flat=True).distinct()
    categories_list = ['All'] + sorted(list(set(all_categories)))

    return render(request, 'blogs.html', {
        'blogs': blogs,
        'query': query,
        'current_category': category or 'All',
        'categories': categories_list,
        'total_blogs': blogs.count()
    })


def blog_detail(request, slug):
    """
    Renders a single official blog post, increments view count, and loads citations.
    """
    blog = get_object_or_404(Blog, slug=slug, is_published=True)

    # Atomically increment views count
    Blog.objects.filter(pk=blog.pk).update(views=F('views') + 1)
    blog.refresh_from_db(fields=['views'])

    # Parse sources / citations
    sources_list = []
    if blog.sources:
        for line in blog.sources.splitlines():
            line = line.strip()
            if line:
                sources_list.append(line)

    # Parse tags
    tags_list = [t.strip() for t in blog.tags.split(',') if t.strip()]

    # Related blogs
    related_blogs = Blog.objects.filter(is_published=True).exclude(pk=blog.pk).order_by('-published_at')[:3]

    return render(request, 'blogview.html', {
        'blog': blog,
        'sources_list': sources_list,
        'tags_list': tags_list,
        'related_blogs': related_blogs
    })