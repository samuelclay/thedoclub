# {% if repo.organization_name %}{{ repo.organization_name }}{% else %}{{ user.login }}{% endif %} / {{ repo.name }}

 * {{ repo.description }}
 * [{{ repo.html_url }}]({{ repo.html_url }})
 * [Languages/frameworks used]

## Background
 
 * {{ user.name }}
 * {% if user.blog %}[{{ user.blog }}]({{ user.blog }}) / {% endif %}@twitterName
 * {% if user.bio %}{{ user.bio }}{% else %}[Your one-line bio -- job, projects, etc]{% endif %}
 