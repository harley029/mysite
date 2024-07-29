from django.views.generic import TemplateView
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rss.models import News
from rss.tasks import news_rss


class RssNews(TemplateView):
    model = News
    template_name = "rss/home.html"
    context_object_name = "rss"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scrap = news_rss()
        articles_list = News.objects.all()
        page = self.request.GET.get("page", 1)

        paginator = Paginator(articles_list, self.paginate_by)
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        context["articles"] = articles
        return context
