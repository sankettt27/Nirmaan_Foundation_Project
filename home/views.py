"""
home/views.py — Views for the public-facing Home (landing page) application.
"""
from django.shortcuts import render


def index(request):
    """
    Render the Nirmaan Foundation public landing page.
    This view is accessible to all visitors, authenticated or not.
    """
    return render(request, 'home/index.html')
