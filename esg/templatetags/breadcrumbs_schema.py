from django import template
from django.utils.safestring import mark_safe
import json

register = template.Library()


@register.simple_tag(takes_context=True)
def breadcrumb_json_ld(context):

    breadcrumbs = context.get('breadcrumbs', [])

    if not breadcrumbs or len(breadcrumbs) <= 1:
        return ''

    request = context.get('request')
    if not request:
        return ''

    # Формируем структуру Schema.org
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": []
    }

    for index, crumb in enumerate(breadcrumbs, start=1):
        item = {
            "@type": "ListItem",
            "position": index,
            "name": crumb.get('label', '')
        }

        # Добавляем URL (кроме последнего элемента)
        if crumb.get('url'):
            item["item"] = request.build_absolute_uri(crumb['url'])

        schema["itemListElement"].append(item)

    json_ld = json.dumps(schema, ensure_ascii=False, indent=2)

    return mark_safe(f'<script type="application/ld+json">\\n{json_ld}\\n</script>')
