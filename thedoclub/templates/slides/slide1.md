{% load presentation_tags %}
## ![]({{ repo.avatar_url }}) {% if repo.organization_name %}{{ repo.organization_name }}{% else %}{{ user.login }}{% endif %} / {{ repo.name }}

 * {{ repo.description }}
 * [{{ repo.html_url }}]({{ repo.html_url }})
 * {% for lang in repo.language_list %}`{{ lang.1|percentage }} {{ lang.0 }}` {% endfor %}

### Background
 
 * {{ user.name }}
 * {% if user.blog %}[{{ user.blog }}]({{ user.blog }}) / {% endif %}[@twitterName](http://twitter.com/thedoclub)
 * {% if user.bio %}{{ user.bio }}{% else %}[Your one-line bio -- job, projects, etc]{% endif %}
 