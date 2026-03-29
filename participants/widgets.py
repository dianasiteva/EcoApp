from django.contrib.admin.widgets import AdminFileWidget
from django.utils.html import format_html


class AdminImagePreviewWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        if value and hasattr(value, "url"):
            html = format_html(
                '<div style="margin-bottom: 10px;"><img src="{}" width="150" style="border-radius: 6px;"/></div>{}',
                value.url,
                html
            )
        return html
