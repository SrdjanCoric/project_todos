{% if is_list_completed(list) %}
  <section id="todos" class="complete">
{% elif is_list_new(list) %}
  <section id="todos" class="new">
{% else %}
  <section id="todos">
{% endif %}