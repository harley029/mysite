from django.urls import path
from rss.views import RssNews

# app_name = "rss"

urlpatterns = [
    path("", RssNews.as_view(), name="rss"),
    path("page/<int:page>/", RssNews.as_view(), name="rss_paginate"),
]
