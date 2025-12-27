# MNO publications

## Pages in this section

<ul>
{% for page in nav.pages %}
  {% if page.url.startswith(page.parent.url) and page.url != page.parent.url %}
    <li>
      <a href="{{ page.url | url }}">{{ page.title }}</a>
    </li>
  {% endif %}
{% endfor %}
</ul>
