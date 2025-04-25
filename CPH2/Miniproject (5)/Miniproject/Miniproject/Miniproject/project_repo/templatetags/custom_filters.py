from django import template

register = template.Library()

@register.filter
def is_image(file_url):
    return file_url.endswith((".png", ".jpg", ".jpeg"))
