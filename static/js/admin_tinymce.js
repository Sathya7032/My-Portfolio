/**
 * TinyMCE Rich Text Editor Integration for Django Admin
 * Enables WYSIWYG editing for Blog description and content fields.
 */
document.addEventListener('DOMContentLoaded', function () {
    if (typeof tinymce === 'undefined') {
        console.warn('TinyMCE library loading from CDN...');
        return;
    }

    // 1. WYSIWYG Editor for Blog Description
    tinymce.init({
        selector: '#id_description',
        height: 240,
        menubar: false,
        plugins: 'advlist autolink lists link charmap preview searchreplace visualblocks code fullscreen wordcount',
        toolbar: 'undo redo | blocks | bold italic underline strikethrough | forecolor backcolor | bullist numlist | link | removeformat | code fullscreen',
        branding: false,
        promotion: false,
        statusbar: true,
        placeholder: 'Write a compelling, formatted summary for preview cards and search results...',
        content_style: 'body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 14px; line-height: 1.6; padding: 8px 12px; }',
        setup: function (editor) {
            editor.on('change keyup', function () {
                editor.save();
            });
        }
    });

    // 2. Full-Featured WYSIWYG Editor for Blog Content
    tinymce.init({
        selector: '#id_content',
        height: 520,
        menubar: 'edit view insert format tools table',
        plugins: 'advlist autolink lists link image charmap preview anchor searchreplace visualblocks code fullscreen insertdatetime media table wordcount codesample help',
        toolbar: 'undo redo | blocks fontfamily fontsize | bold italic underline strikethrough | forecolor backcolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image media codesample table | removeformat | code fullscreen',
        branding: false,
        promotion: false,
        codesample_languages: [
            { text: 'HTML/XML', value: 'markup' },
            { text: 'JavaScript', value: 'javascript' },
            { text: 'CSS', value: 'css' },
            { text: 'Python', value: 'python' },
            { text: 'Java', value: 'java' },
            { text: 'SQL', value: 'sql' },
            { text: 'Bash / Shell', value: 'bash' },
            { text: 'JSON', value: 'json' }
        ],
        statusbar: true,
        placeholder: 'Compose full technical article with code blocks, headings, images, and formatted sections...',
        content_style: 'body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.7; padding: 12px 16px; }',
        setup: function (editor) {
            editor.on('change keyup', function () {
                editor.save();
            });
        }
    });

    // Ensure editor content syncs back to Django textarea prior to submission
    const form = document.querySelector('form#blog_form') || document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function () {
            if (typeof tinymce !== 'undefined') {
                tinymce.triggerSave();
            }
        });
    }
});
