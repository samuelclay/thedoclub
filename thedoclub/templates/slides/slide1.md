{% load presentation_tags %}
## ![]({{ repo.avatar_url }}) {% if repo.organization_name %}{{ repo.organization_name }}{% else %}{{ repo.owner_name }}{% endif %} / {{ repo.name }}

 * {{ repo.description }}
 * [{{ repo.html_url }}]({{ repo.html_url }})
 * {% for lang in repo.language_list %}`{{ lang.1|percentage }} {{ lang.0 }}` {% endfor %}

### Background
 
 * {{ user.name }} &middot; [{{ user.email }}](mailto:{{ user.email }})
 * {% if user.blog %}[{{ user.blog }}]({{ user.blog }}) &middot; {% endif %}[@twitterName](http://twitter.com/thedoclub)
 * {% if user.bio %}{{ user.bio }}{% else %}[Your one-line bio -- job, projects, etc]{% endif %}
 