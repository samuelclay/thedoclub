# {{ repo.name }}

## Background
 
 * {{ user.name }}{% if user.blog %}
 * ({{ user.blog }})[{{ user.blog }}]{% endif %}
 * {% if user.bio %}{{ user.bio }}{% else %}[Your one-line bio -- job, projects, etc]{% endif %}
 
## {% if repo.organization_name %}{{ repo.organization_name }} / {% endif %}{{ repo.name }}

 * {{ repo.description }}
 * ({{ repo.html_url }})[{{ repo.html_url }}]
 * [Languages/frameworks used]
