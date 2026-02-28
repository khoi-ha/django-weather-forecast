from django.contrib import admin
from django.utils.html import format_html
from .models import Background
# Register your models here.

@admin.register(Background)
class BackgroundAdmin(admin.ModelAdmin):
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        """Generate an HTML image tag for the background image preview.

        Args:
            obj (Background): The Background object to generate the preview for.

        Returns:
            _type_: _description_
        """
        if obj.link:
            return format_html(
                '<img src="{}" style="max-height: 240px; border-radius: 8px;" />',
                obj.link
            )
        return "Save and continue editing to see preview."

    image_preview.short_description = "Preview"