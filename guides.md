---
layout: page
title: お金と経済の解説
headline: 金利・物価・為替・住宅ローンを、ニュースに左右されない基礎から解説します。
permalink: /guides/
lang: ja
has_en_version: false
---

ニュースで繰り返し登場する金利、物価、為替、住宅ローンの仕組みを、家計への影響まで含めて整理しています。発表直後の値動きを予想する記事ではなく、数カ月先にも使える読み方をまとめた解説です。

<div class="guide-list">
{% assign guide_count = 0 %}
{% for post in site.posts %}
  {% if post.categories contains "解説" %}
  {% assign guide_count = guide_count | plus: 1 %}
  <article class="guide-card">
    <p class="guide-card-meta">{{ post.date | date: "%Y年%-m月%-d日" }}</p>
    <h2><a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a></h2>
    <p>{{ post.headline | default: post.excerpt | strip_html | normalize_whitespace | escape }}</p>
  </article>
  {% endif %}
{% endfor %}
</div>

{% if guide_count == 0 %}
解説記事は準備中です。
{% endif %}
