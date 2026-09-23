from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class ContactMessage(models.Model):
    """
    Stores contact form submissions received from visitors on the portfolio.
    """
    name = models.CharField(max_length=150, verbose_name="Sender Name")
    email = models.EmailField(verbose_name="Sender Email")
    subject = models.CharField(max_length=200, verbose_name="Subject / Inquiry Type")
    message = models.TextField(verbose_name="Transmission Message")
    is_read = models.BooleanField(default=False, verbose_name="Mark as Read")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Received At")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.created_at.strftime('%d %b %Y %H:%M')})"


class Blog(models.Model):
    """
    Official Tech Blogs authored by K Satyanarayana Chary (@sathya).
    """
    title = models.CharField(max_length=255, verbose_name="Article Title")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="URL Slug")
    description = models.TextField(help_text="Concise summary for preview cards, social shares, and SEO.", verbose_name="Short Summary")
    content = models.TextField(help_text="Full article body (Supports rich HTML / Markdown formatted text).", verbose_name="Article Content")
    author = models.CharField(max_length=120, default="K Satyanarayana Chary (@sathya)", verbose_name="Author")
    category = models.CharField(max_length=80, default="Engineering", verbose_name="Category / Domain")
    tags = models.CharField(max_length=200, default="Spring Boot, React Native, AWS", help_text="Comma-separated tags (e.g. Java, AWS, Mobile)", verbose_name="Tags")
    image = models.ImageField(upload_to="blogs/%Y/%m/", blank=True, null=True, verbose_name="Cover Image Upload")
    image_url = models.URLField(blank=True, null=True, help_text="Optional fallback image URL if not uploading file.", verbose_name="Image URL Fallback")
    views = models.PositiveIntegerField(default=0, verbose_name="Total Views")
    read_time = models.CharField(max_length=40, default="5 min read", verbose_name="Estimated Read Time")
    sources = models.TextField(blank=True, help_text="References, documentation links, citations, or GitHub repositories (one per line or comma-separated).", verbose_name="References & Sources")
    is_published = models.BooleanField(default=True, verbose_name="Published Status")
    published_at = models.DateTimeField(default=timezone.now, verbose_name="Published Date & Time")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    class Meta:
        ordering = ['-published_at']
        verbose_name = "Blog Article"
        verbose_name_plural = "Blog Articles"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Blog.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_cover_image(self):
        """Returns uploaded image URL or fallback URL or default static asset."""
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return "/static/img/avatar.jpg"

    def __str__(self):
        return self.title
