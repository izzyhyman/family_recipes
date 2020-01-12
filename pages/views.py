from django.shortcuts import render
from django.views.generic import TemplateView


class AboutPageView(TemplateView):
    '''View for the About page'''
    template_name = "about.html"

