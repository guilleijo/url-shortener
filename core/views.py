from django.views import generic, View
from django.shortcuts import render

class HomeView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        pass
