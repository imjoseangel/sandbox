from django.urls import path

from redditbot.reddit.views import lead_view

app_name = "reddit"

urlpatterns = [

    path("leads/", view=lead_view, name="leads"),

]
