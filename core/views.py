from django.contrib import messages
from django.urls import reverse
from django.views import View
from django.shortcuts import render, redirect
from django.core.exceptions import MultipleObjectsReturned

from core.models import Url
from core.forms import UrlForm
from core.constants import ALREADY_USED_MESSAGE, NOT_FOUND_MESSAGE


class HomeView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = UrlForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        url = form.cleaned_data.get('url')
        hashed_url = form.cleaned_data.get('hashed_url')

        if hashed_url:
            obj, created = Url.objects.get_or_create(
                hashed_url=hashed_url,
                defaults={'url': url},
            )
            if not created and obj.url != url:
                messages.error(request, ALREADY_USED_MESSAGE)
                return render(
                    request,
                    self.template_name,
                    {'form': form},
                )
        else:
            try:
                obj, _ = Url.objects.get_or_create(url=url)
            except MultipleObjectsReturned:
                obj = Url.objects.filter(url=url).first()

        return render(
            request, self.template_name, {'short_url': obj.get_full_short_url()}
        )


class RedirectView(View):
    def get(self, request, *args, **kwargs):
        hashed_url = kwargs.get('hash')
        try:
            obj = Url.objects.get(hashed_url=hashed_url)
        except Url.DoesNotExist:
            messages.error(request, NOT_FOUND_MESSAGE)
            return redirect(reverse('home_page'))

        return redirect(obj.url)
