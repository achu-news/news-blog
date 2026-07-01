---
layout: page
permalink: /archive/
---

{% if site.active_lang == "en" %}
# Archive
{% else %}
# 過去の記事一覧
{% endif %}

{% assign date_format = "%Y年%-m月" %}
{% if site.active_lang == "en" %}{% assign date_format = "%B %Y" %}{% endif %}
{% assign prev_month = "" %}
{% for post in site.posts %}
{% assign this_month = post.date | date: date_format %}
{% if this_month != prev_month %}
## {{ this_month }}
{% assign prev_month = this_month %}
{% endif %}
- {{ post.date | date: "%m/%d" }} — [{{ post.headline | default: post.title }}]({{ post.url | relative_url }})
{% endfor %}
