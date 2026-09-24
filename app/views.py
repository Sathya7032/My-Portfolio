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

    # Other blogs excluding current
    other_blogs = Blog.objects.filter(is_published=True).exclude(pk=blog.pk).order_by('-published_at')[:4]

    # Popular blogs by views excluding current
    popular_blogs = Blog.objects.filter(is_published=True).exclude(pk=blog.pk).order_by('-views')[:3]

    # All distinct categories
    all_categories = Blog.objects.filter(is_published=True).values_list('category', flat=True).distinct()
    categories_list = sorted(list(set(all_categories)))

    return render(request, 'blogview.html', {
        'blog': blog,
        'sources_list': sources_list,
        'tags_list': tags_list,
        'related_blogs': other_blogs,
        'other_blogs': other_blogs,
        'popular_blogs': popular_blogs,
        'categories_list': categories_list,
    })


# -------------------------------------------------------------
# NEO-BRUTALIST ADMIN DASHBOARD VIEWS
# -------------------------------------------------------------
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum, Count
# pyrefly: ignore [missing-import]
from .forms import BlogForm


def staff_required(view_func):
    """Decorator ensuring only authenticated staff/superusers can access dashboard views."""
    return user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='/dashboard/login/')(view_func)


def dashboard_login(request):
    """
    Renders Neo-Brutalist authentication page for admin access.
    """
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard_index')

    error_msg = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            auth_login(request, user)
            next_url = request.GET.get('next') or 'dashboard_index'
            messages.success(request, f"Welcome back, Commander {user.username}!")
            return redirect(next_url)
        else:
            error_msg = "Invalid admin credentials or insufficient staff authorization."

    return render(request, 'dashboard/login.html', {
        'error_msg': error_msg
    })


def dashboard_logout(request):
    """
    Logs out the admin and redirects to the login screen.
    """
    auth_logout(request)
    messages.info(request, "Logged out of admin console.")
    return redirect('dashboard_login')


@staff_required
def dashboard_index(request):
    """
    Main Neo-Brutalist Dashboard Overview: KPIs, stats, quick actions, and recent activity.
    """
    total_blogs = Blog.objects.count()
    published_blogs = Blog.objects.filter(is_published=True).count()
    draft_blogs = total_blogs - published_blogs
    total_views = Blog.objects.aggregate(total=Sum('views'))['total'] or 0

    total_messages = ContactMessage.objects.count()
    unread_messages = ContactMessage.objects.filter(is_read=False).count()

    recent_blogs = Blog.objects.all().order_by('-created_at')[:5]
    recent_messages = ContactMessage.objects.all().order_by('-created_at')[:5]

    top_categories = Blog.objects.values('category').annotate(count=Count('id')).order_by('-count')[:5]

    return render(request, 'dashboard/index.html', {
        'total_blogs': total_blogs,
        'published_blogs': published_blogs,
        'draft_blogs': draft_blogs,
        'total_views': total_views,
        'total_messages': total_messages,
        'unread_messages': unread_messages,
        'recent_blogs': recent_blogs,
        'recent_messages': recent_messages,
        'top_categories': top_categories,
    })


@staff_required
def dashboard_blogs(request):
    """
    Blog Management: Lists all articles with search, status filters, views, and action controls.
    """
    query = request.GET.get('q', '').strip()
    status = request.GET.get('status', 'all').strip()
    category = request.GET.get('category', '').strip()

    blogs = Blog.objects.all()

    if query:
        blogs = blogs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query) |
            Q(tags__icontains=query)
        )

    if status == 'published':
        blogs = blogs.filter(is_published=True)
    elif status == 'draft':
        blogs = blogs.filter(is_published=False)

    if category:
        blogs = blogs.filter(category__iexact=category)

    # Categories for filter dropdown
    all_categories = sorted(list(set(Blog.objects.values_list('category', flat=True).distinct())))

    return render(request, 'dashboard/blogs.html', {
        'blogs': blogs,
        'query': query,
        'current_status': status,
        'current_category': category,
        'categories': all_categories,
        'total_count': Blog.objects.count(),
        'published_count': Blog.objects.filter(is_published=True).count(),
        'draft_count': Blog.objects.filter(is_published=False).count(),
    })


@staff_required
def dashboard_blog_create(request):
    """
    Creates a new blog article with rich Neo-Brutalist editor.
    """
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save()
            messages.success(request, f"Article '{blog.title}' has been successfully created!")
            return redirect('dashboard_blogs')
    else:
        form = BlogForm()

    return render(request, 'dashboard/blog_form.html', {
        'form': form,
        'action_title': 'NEW ARTICLE TRANSMISSION',
        'is_edit': False,
    })


@staff_required
def dashboard_blog_edit(request, pk):
    """
    Edits an existing blog article.
    """
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, f"Article '{blog.title}' updated successfully!")
            return redirect('dashboard_blogs')
    else:
        form = BlogForm(instance=blog)

    return render(request, 'dashboard/blog_form.html', {
        'form': form,
        'blog': blog,
        'action_title': f"EDIT TRANSMISSION // {blog.title}",
        'is_edit': True,
    })


@staff_required
def dashboard_blog_toggle(request, pk):
    """
    Toggles an article's published status (Published <-> Draft).
    """
    blog = get_object_or_404(Blog, pk=pk)
    blog.is_published = not blog.is_published
    blog.save(update_fields=['is_published'])
    status_label = "PUBLISHED" if blog.is_published else "DRAFTED"
    messages.success(request, f"Article '{blog.title}' is now {status_label}.")
    return redirect(request.META.get('HTTP_REFERER', 'dashboard_blogs'))


@staff_required
def dashboard_blog_delete(request, pk):
    """
    Deletes a blog article.
    """
    blog = get_object_or_404(Blog, pk=pk)
    title = blog.title
    blog.delete()
    messages.success(request, f"Article '{title}' deleted.")
    return redirect('dashboard_blogs')


@staff_required
def dashboard_messages(request):
    """
    Inquiries / Contact Messages Inbox: Filter by all/unread/read and search transmissions.
    """
    status = request.GET.get('status', 'all').strip()
    query = request.GET.get('q', '').strip()

    messages_qs = ContactMessage.objects.all()

    if query:
        messages_qs = messages_qs.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(subject__icontains=query) |
            Q(message__icontains=query)
        )

    if status == 'unread':
        messages_qs = messages_qs.filter(is_read=False)
    elif status == 'read':
        messages_qs = messages_qs.filter(is_read=True)

    return render(request, 'dashboard/messages.html', {
        'contact_messages': messages_qs,
        'current_status': status,
        'query': query,
        'total_count': ContactMessage.objects.count(),
        'unread_count': ContactMessage.objects.filter(is_read=False).count(),
        'read_count': ContactMessage.objects.filter(is_read=True).count(),
    })


@staff_required
def dashboard_message_toggle(request, pk):
    """
    Toggles a contact message read / unread status.
    """
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.is_read = not msg.is_read
    msg.save(update_fields=['is_read'])
    state = "marked as READ" if msg.is_read else "marked as UNREAD"
    messages.success(request, f"Message from {msg.name} {state}.")
    return redirect(request.META.get('HTTP_REFERER', 'dashboard_messages'))


@staff_required
def dashboard_message_delete(request, pk):
    """
    Deletes a contact transmission.
    """
    msg = get_object_or_404(ContactMessage, pk=pk)
    sender = msg.name
    msg.delete()
    messages.success(request, f"Message from {sender} deleted.")
    return redirect('dashboard_messages')