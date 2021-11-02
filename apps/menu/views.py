from django.views.generic import DetailView
from apps.menu.models import TextPage


class TextPageView(DetailView):
    template_name = 'textpage.html'
    model = TextPage
