from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import TemplateView
from . import forms
from . import models

from .forms import NewCountryForm
# Create your views here.

class IndexView(TemplateView):
    template_name = "index.html"


class SuccessView(TemplateView):
    template_name = "success.html"


class NewCountryView(CreateView):
    model = models.Country
    form_class = forms.NewCountryForm
    success_url = reverse_lazy("politeum:success")