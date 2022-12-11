from django.urls import path

from reddit_bot.reddit.views import lead_view

app_name = "reddit"

urlpatterns = [

    path("leads/", view=lead_view, name="leads"),

]
