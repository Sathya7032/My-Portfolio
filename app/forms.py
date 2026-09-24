from django import forms
# pyrefly: ignore [missing-import]
from .models import Blog


class BlogForm(forms.ModelForm):
    """
    Neo-Brutalist form for creating and updating blog articles in the custom admin dashboard.
    """
    class Meta:
        model = Blog
        fields = [
            'title', 'slug', 'category', 'tags', 'read_time',
            'author', 'description', 'content', 'sources',
            'image', 'image_url', 'is_published'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 font-sans font-bold text-sm bg-white dark:bg-brutal-cardDark text-brutal-black dark:text-white border-2 border-brutal-black focus:outline-none focus:ring-2 focus:ring-neon-cyan brutal-box-sm',
                'placeholder': 'e.g. Zero-Downtime Microservices with Java Spring Boot and AWS',
                'required': True,
                'id': 'id_title'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 font-mono text-xs bg-white dark:bg-brutal-cardDark text-brutal-black dark:text-white border-2 border-brutal-black focus:outline-none focus:ring-2 focus:ring-neon-cyan brutal-box-sm',
                'placeholder': 'leave-blank-to-auto-generate-from-title',
                'id': 'id_slug'
            }),
            'category': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 font-mono text-xs font-bold bg-white dark:bg-brutal-cardDark text-brutal-black dark:text-white border-2 border-brutal-black focus:outline-none focus:ring-2 focus:ring-neon-cyan brutal-box-sm',
                'placeholder': 'e.g. Cloud & Architecture, Mobile & Backend, Game Development',
                'required': True,
                'id': 'id_category'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 font-mono text-xs bg-white dark:bg-brutal-cardDark text-brutal-black dark:text-white border-2 border-brutal-black focus:outline-none focus:ring-2 focus:ring-neon-cyan brutal-box-sm',
                'placeholder': 'Comma-separated (e.g. Java, Spring Boot, AWS, Docker)',
                'id': 'id_tags'
            }),
            'read_time': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 font-mono text-xs bg-white dark:bg-brutal-cardDark text-brutal-black dark:text-white border-2 border-brutal-black focus:outline-none focus:ring-2 focus:ring-neon-cyan brutal-box-sm',
                'placeholder': 'e.g. 5 min read',
                'id': 'id_read_time'
            }),
            'author': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 font-sans font-bold text-xs bg-white dark:bg-brutal-cardDark text-brutal-black dark:text-white border-2 border-brutal-black focus:outline-none focus:ring-2 focus:ring-neon-cyan brutal-box-sm',
                'placeholder': 'K Satyanarayana Chary (@sathya)',
                'id': 'id_author'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2.5 font-sans text-sm bg-white dark:bg-brutal-cardDark text-brutal-black dark:text-white border-2 border-brutal-black focus:outline-none focus:ring-2 focus:ring-neon-cyan brutal-box-sm leading-relaxed',
                'rows': 3,
                'placeholder': 'High-impact summary for preview cards, social sharing, and search engine optimization...',
                'required': True,
                'id': 'id_description'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2.5 font-sans text-sm bg-white dark:bg-brutal-cardDark text-brutal-black dark:text-white border-2 border-brutal-black focus:outline-none focus:ring-2 focus:ring-neon-cyan brutal-box-sm tinymce-target',
                'rows': 16,
                'placeholder': 'Write rich article content here (HTML supported)...',
                'id': 'id_content'
            }),
            'sources': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2.5 font-mono text-xs bg-white dark:bg-brutal-cardDark text-brutal-black dark:text-white border-2 border-brutal-black focus:outline-none focus:ring-2 focus:ring-neon-cyan brutal-box-sm',
                'rows': 3,
                'placeholder': 'https://github.com/...\nhttps://docs.spring.io/...\n(One link per line)',
                'id': 'id_sources'
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2.5 font-mono text-xs bg-white dark:bg-brutal-cardDark text-brutal-black dark:text-white border-2 border-brutal-black focus:outline-none focus:ring-2 focus:ring-neon-cyan brutal-box-sm',
                'placeholder': 'https://images.unsplash.com/... (optional fallback)',
                'id': 'id_image_url'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 font-mono text-xs bg-white dark:bg-brutal-cardDark text-brutal-black dark:text-white border-2 border-brutal-black cursor-pointer',
                'id': 'id_image'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 accent-neon-yellow border-2 border-brutal-black cursor-pointer rounded-none',
                'id': 'id_is_published'
            }),
        }
