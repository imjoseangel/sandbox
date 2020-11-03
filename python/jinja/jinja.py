from jinja2 import Template
from jinja2 import Environment

env = Environment(variable_start_string="[%", variable_end_string="%]")
tmpl = env.from_string('Hello [% name %]!')
y = tmpl.render(name="John Doe")

t = Template("Hello {{ something }}!")
x = t.render(something="World")
print(y)
