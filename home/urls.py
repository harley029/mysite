from django.urls import path
from home.views import HomeView, OurTeamView, AppFeaturesView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("our_team", OurTeamView.as_view(), name="our_team"),
    path("features", AppFeaturesView.as_view(), name="app_features"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
