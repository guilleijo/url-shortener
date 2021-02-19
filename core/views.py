from django.views import generic, View
from django.shortcuts import render, redirect
from django.core.exceptions import MultipleObjectsReturned

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
            hashed_url = form.cleaned_data.get('hashed_url')
            
            if hashed_url:
                obj = Url.objects.filter(hashed_url=hashed_url).first()
                if obj is not None and obj.url != url:
                    context = {'error': 'Hash already in use'}
                elif obj is not None and obj.url == url:
                    context = {'short_url': obj.get_full_short_url()}
                else:
                    obj, _ = Url.objects.get_or_create(url=url, hashed_url=hashed_url)
                    context = {'short_url': obj.get_full_short_url()}
                return render(request, self.template_name, context)

            try:
                obj, _ = Url.objects.get_or_create(url=url)
            except MultipleObjectsReturned:
                obj = Url.objects.filter(url=url).first()

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
