from django.views import generic, View
from django.shortcuts import render, redirect

from core.models import Url
from core.forms import UrlForm


class HomeView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = UrlForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data.get('url')

            obj, _ = Url.objects.get_or_create(url=url)
            full_short_url = obj.get_full_short_url()
            context = {'short_url': full_short_url}

            return render(request, self.template_name, context)

        return render(request, self.template_name, {"form": form})


class RedirectView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        hashed_url = kwargs.get('hash')
        try:
            obj = Url.objects.get(hashed_url=hashed_url)
        except Url.DoesNotExist:
            context = {'error': 'Not found'}
            return render(request, self.template_name, context)

        return redirect(obj.url)
