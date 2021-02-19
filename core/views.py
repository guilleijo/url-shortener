from django.views import generic, View
from django.shortcuts import render, redirect

from core.models import Url


class HomeView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        pass

class RedirectView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        short_url = kwargs.get('shorturl')
        try:
            obj = Url.objects.get(short_url=short_url)
        except Url.DoesNotExist:
            context = {'error': 'Not found'}
            return render(request, self.template_name, context)

        return redirect(obj.url)
