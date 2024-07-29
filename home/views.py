from django.views.generic import View
from django.shortcuts import render


class HomeView(View):

    def get(self, request):
        return render(request, "home/home.html")


class OurTeamView(View):

    def get(self, request):
        return render(request, "home/our_team.html")


class AppFeaturesView(View):

    def get(self, request):
        return render(request, "home/home_features.html")


