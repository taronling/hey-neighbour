# In a file called [project root]/components/calendar/calendar.py
from django_components import component

@component.register("card")
class Card(component.Component):
    # Templates inside `[your apps]/components` dir and `[project root]/components` dir will be automatically found. To customize which template to use based on context
    # you can override def get_template_name() instead of specifying the below variable.
    template_name = "card/card.html"

    # This component takes one parameter, a date string to show in the template

    class Media:
        css = "website/components/card/card.css"
        js = "website/components/card/card.js"
        